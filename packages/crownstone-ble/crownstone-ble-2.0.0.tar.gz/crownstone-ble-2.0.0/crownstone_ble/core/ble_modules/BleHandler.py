import asyncio
import logging

from bleak import BleakClient, BleakScanner

from crownstone_core.Exceptions import CrownstoneBleException
from crownstone_core.core.modules.EncryptionSettings import EncryptionSettings
from crownstone_core.protocol.BluenetTypes import ProcessType
from crownstone_core.util.EncryptionHandler import EncryptionHandler

from crownstone_ble.Exceptions import BleError
from crownstone_ble.core.BleEventBus import BleEventBus

from crownstone_ble.core.bluetooth_delegates.BleakScanDelegate import BleakScanDelegate
from crownstone_ble.core.bluetooth_delegates.NotificationDelegate import NotificationDelegate
from crownstone_ble.core.modules.Validator import Validator
from crownstone_ble.topics.SystemBleTopics import SystemBleTopics

_LOGGER = logging.getLogger(__name__)

CCCD_UUID = 0x2902


class ActiveClient:

    def __init__(self, address, cleanupCallback, bleAdapterAddress):
        self.address = address
        self.client = BleakClient(address, adapter=bleAdapterAddress)
        self.services = None
        self.cleanupCallback = cleanupCallback
        self.client.set_disconnected_callback(self.forcedDisconnect)

    def forcedDisconnect(self, data):
        BleEventBus.emit(SystemBleTopics.forcedDisconnect, self.address)
        self.cleanupCallback()

    async def isConnected(self):
        return await self.client.is_connected()



class BleHandler:

    def __init__(self, settings: EncryptionSettings, bleAdapterAddress: str=None):
        # bleAdapterAddress is the MAC address of the adapter you want to use.
        self.activeClient = None
        self.connectedPeripherals = {}
        self.settings = settings

        self.scanner = BleakScanner(adapter=bleAdapterAddress)
        self.scanningActive = False
        self.scanAborted = False
        scanDelegate = BleakScanDelegate(self.settings)
        self.scanner.register_detection_callback(scanDelegate.handleDiscovery)

        self.bleAdapterAddress = bleAdapterAddress

        self.notificationLoopActive = False
        self.subscriptionIds = []

        self.validator = Validator()
        self.subscriptionIds.append(BleEventBus.subscribe(SystemBleTopics.abortScanning, lambda x: self.abortScan()))


    async def shutDown(self):
        for subscriptionId in self.subscriptionIds:
            BleEventBus.unsubscribe(subscriptionId)
        await self.disconnect()
        await self.stopScanning()


    async def is_connected_guard(self):
        connected = await self.is_connected()
        if not connected:
            _LOGGER.debug(f"Could not perform action since the client is not connected!.")
            raise CrownstoneBleException("Not connected.")


    async def is_connected(self):
        if self.activeClient is not None:
            connected = await self.activeClient.client.is_connected()
            if connected:
                return True
        return False


    def resetClient(self):
        self.activeClient = None


    async def connect(self, address) -> bool:
        self.activeClient = ActiveClient(address, lambda: self.resetClient(), self.bleAdapterAddress)
        _LOGGER.info(f"Connecting to {address}")
        # this can throw an error when the connection fails.
        # these BleakErrors are nicely human readable.
        # TODO: document/convert these errors.
        connected  = await self.activeClient.client.connect()
        serviceSet = await self.activeClient.client.get_services()
        self.activeClient.services = serviceSet.services

        return connected
        # print(self.activeClient.client.services.characteristics)


    async def disconnect(self):
        if self.activeClient is not None:
            await self.activeClient.client.disconnect()
            self.activeClient = None


    async def waitForPeripheralToDisconnect(self, timeout: int = 10):
        if self.activeClient is not None:
            if await self.activeClient.isConnected():
                waiting = True
                def disconnectListener(data):
                    nonlocal waiting
                    waiting = False

                listenerId = BleEventBus.subscribe(SystemBleTopics.forcedDisconnect, disconnectListener)

                timer = 0
                while waiting and timer < 10:
                    await asyncio.sleep(0.1)
                    timer += 0.1

                BleEventBus.unsubscribe(listenerId)

                self.activeClient = None


    async def scan(self, duration=3):
        await self.startScanning()
        while duration > 0 and self.scanAborted == False:
            await asyncio.sleep(0.1)
            duration -= 0.1
        await self.stopScanning()


    async def startScanning(self):
        if not self.scanningActive:
            self.scanAborted = False
            self.scanningActive = True
            await self.scanner.start()


    async def stopScanning(self):
        if self.scanningActive:
            self.scanningActive = False
            self.scanAborted = False
            await self.scanner.stop()


    def abortScan(self):
        self.scanAborted = True


    async def writeToCharacteristic(self, serviceUUID, characteristicUUID, content):
        _LOGGER.debug(f"writeToCharacteristic serviceUUID={serviceUUID} characteristicUUID={characteristicUUID} content={content}")
        await self.is_connected_guard()
        encryptedContent = EncryptionHandler.encrypt(content, self.settings)
        payload = self._preparePayload(encryptedContent)
        await self.activeClient.client.write_gatt_char(characteristicUUID, payload, response=True)


    async def writeToCharacteristicWithoutEncryption(self, serviceUUID, characteristicUUID, content):
        _LOGGER.debug(f"writeToCharacteristicWithoutEncryption serviceUUID={serviceUUID} characteristicUUID={characteristicUUID} content={content}")
        await self.is_connected_guard()
        payload = self._preparePayload(content)
        await self.activeClient.client.write_gatt_char(characteristicUUID, payload, response=True)


    async def readCharacteristic(self, serviceUUID, characteristicUUID):
        _LOGGER.debug(f"readCharacteristic serviceUUID={serviceUUID} characteristicUUID={characteristicUUID}")
        data = await self.readCharacteristicWithoutEncryption(serviceUUID, characteristicUUID)
        if self.settings.isEncryptionEnabled():
            return EncryptionHandler.decrypt(data, self.settings)


    async def readCharacteristicWithoutEncryption(self, serviceUUID, characteristicUUID):
        _LOGGER.debug(f"readCharacteristicWithoutEncryption serviceUUID={serviceUUID} characteristicUUID={characteristicUUID}")
        await self.is_connected_guard()
        return await self.activeClient.client.read_gatt_char(characteristicUUID)


    async def setupSingleNotification(self, serviceUUID, characteristicUUID, writeCommand):
        _LOGGER.debug(f"setupSingleNotification serviceUUID={serviceUUID} characteristicUUID={characteristicUUID}")
        await self.is_connected_guard()

        # setup the collecting of the notification data.
        notificationDelegate = NotificationDelegate(self._killNotificationLoop, self.settings)
        await self.activeClient.client.start_notify(characteristicUUID, notificationDelegate.handleNotification)

        # execute something that will trigger the notifications
        await writeCommand()

        # wait for the results to come in.
        self.notificationLoopActive = True
        loopCount = 0
        while self.notificationLoopActive and loopCount < 50:
            await asyncio.sleep(0.25)
            loopCount += 1


        if notificationDelegate.result is None:
            raise CrownstoneBleException(BleError.NO_NOTIFICATION_DATA_RECEIVED, "No notification data received.")

        connected = await self.is_connected()
        if connected:
            await self.activeClient.client.stop_notify(characteristicUUID)

        return notificationDelegate.result


    async def setupNotificationStream(self, serviceUUID, characteristicUUID, writeCommand, resultHandler, timeout):
        _LOGGER.debug(f"setupNotificationStream serviceUUID={serviceUUID} characteristicUUID={characteristicUUID} timeout={timeout}")
        await self.is_connected_guard()

        # setup the collecting of the notification data.
        notificationDelegate = NotificationDelegate(self._killNotificationLoop, self.settings)
        await self.activeClient.client.start_notify(characteristicUUID, notificationDelegate.handleNotification)

        # execute something that will trigger the notifications
        await writeCommand()

        # wait for the results to come in.
        self.notificationLoopActive = True
        loopCount = 0
        successful = False
        while self.notificationLoopActive and loopCount < timeout*4:
            await asyncio.sleep(0.25)
            loopCount += 1
            if notificationDelegate.result is not None:
                command = resultHandler(notificationDelegate.result)
                notificationDelegate.result = None
                if command == ProcessType.ABORT_ERROR:
                    self.notificationLoopActive = False
                    raise CrownstoneBleException(BleError.ABORT_NOTIFICATION_STREAM_W_ERROR, "Aborting the notification stream because the resultHandler raised an error.")
                elif command == ProcessType.FINISHED:
                    self.notificationLoopActive = False
                    successful = True

        if not successful:
            raise CrownstoneBleException(BleError.NOTIFICATION_STREAM_TIMEOUT, "Notification stream not finished within timeout.")

        # remove subscription from this characteristic
        connected = await self.is_connected()
        if connected:
            await self.activeClient.client.stop_notify(characteristicUUID)


    def _killNotificationLoop(self):
        self.notificationLoopActive = False


    def _preparePayload(self, data: list or bytes or bytearray):
        return bytearray(data)
