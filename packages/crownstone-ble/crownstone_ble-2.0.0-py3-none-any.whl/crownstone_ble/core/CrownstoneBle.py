import logging

from crownstone_ble.core.container.ScanData import ScanData

from crownstone_ble.core.ble_modules.BleHandler import BleHandler
from crownstone_ble.topics.BleTopics import BleTopics
from crownstone_core.Exceptions import CrownstoneError, CrownstoneBleException, CrownstoneException
from crownstone_core.core.modules.EncryptionSettings import EncryptionSettings
from crownstone_core.util.JsonFileStore import JsonFileStore

from crownstone_ble.Exceptions import BleError
from crownstone_ble.core.BleEventBus import BleEventBus
from crownstone_ble.core.ble_modules.ControlHandler import ControlHandler
from crownstone_ble.core.ble_modules.SetupHandler import SetupHandler
from crownstone_ble.core.ble_modules.StateHandler import StateHandler
from crownstone_ble.core.ble_modules.DebugHandler import DebugHandler
from crownstone_ble.core.modules.Gatherer import Gatherer
from crownstone_ble.core.modules.NearestSelector import NearestSelector
from crownstone_ble.core.modules.NormalModeChecker import NormalModeChecker
from crownstone_ble.core.modules.RssiChecker import RssiChecker
from crownstone_ble.core.modules.SetupChecker import SetupChecker

_LOGGER = logging.getLogger(__name__)

class CrownstoneBle:
    __version__ = "2.0.0"
    
    def __init__(self, bleAdapterAddress: str = None):
        # bleAdapterAddress is the MAC address of the adapter you want to use.
        self.settings  = EncryptionSettings()
        self.control   = ControlHandler(self)
        self.setup     = SetupHandler(self)
        self.state     = StateHandler(self)
        self.debug     = DebugHandler(self)
        self.ble       = BleHandler(self.settings, bleAdapterAddress)

        self.defaultKeysOverridden = False

        # load default keys so the lib won't crash if you don't use keys.
        self.settings.loadKeys("adminKeyForCrown", "memberKeyForHome", "basicKeyForOther", "MyServiceDataKey", "aLocalizationKey", "MyGoodMeshAppKey", "MyGoodMeshNetKey")

    async def shutDown(self):
        await self.ble.shutDown()
    
    def setSettings(self, adminKey, memberKey, basicKey, serviceDataKey, localizationKey, meshApplicationKey, meshNetworkKey):
        self.settings.loadKeys(adminKey, memberKey, basicKey, serviceDataKey, localizationKey, meshApplicationKey, meshNetworkKey)
        self.defaultKeysOverridden = True

    def loadSettingsFromDictionary(self, data):
        if "admin" not in data:
            raise CrownstoneBleException(CrownstoneError.ADMIN_KEY_REQURED)
        if "member" not in data:
            raise CrownstoneBleException(CrownstoneError.MEMBER_KEY_REQUIRED)
        if "basic" not in data:
            raise CrownstoneBleException(CrownstoneError.BASIC_KEY_REQURED)
        if "serviceDataKey" not in data:
            raise CrownstoneBleException(CrownstoneError.SERVICE_DATA_KEY_REQUIRED)
        if "localizationKey" not in data:
            raise CrownstoneBleException(CrownstoneError.LOCALIZATION_KEY_REQUIRED)
        if "meshApplicationKey" not in data:
            raise CrownstoneBleException(CrownstoneError.MESH_APP_KEY)
        if "meshNetworkKey" not in data:
            raise CrownstoneBleException(CrownstoneError.MESH_NETWORK_KEY)

        self.setSettings(data["admin"], data["member"], data["basic"], data["serviceDataKey"], data["localizationKey"],
                         data["meshApplicationKey"], data["meshNetworkKey"])

    def loadSettingsFromFile(self, path):
        fileReader = JsonFileStore(path)
        data = fileReader.getData()
        self.loadSettingsFromDictionary(data)


    async def connect(self, address, ignoreEncryption=False):
        await self.ble.connect(address)
        if not ignoreEncryption:
            try:
                await self.control.getAndSetSessionNone()
            except CrownstoneBleException as err:
                # the only relevant error here is this one. If it is any other, the Crownstone is in the wrong mode
                if err.type is BleError.COULD_NOT_VALIDATE_SESSION_NONCE:
                    raise err


    async def setupCrownstone(self, address, sphereId, crownstoneId, meshDeviceKey, ibeaconUUID, ibeaconMajor, ibeaconMinor):
        if not self.defaultKeysOverridden:
            raise CrownstoneBleException(BleError.NO_ENCRYPTION_KEYS_SET,
                                         "Keys are not initialized so I can't put anything on the Crownstone. Make sure you call .setSettings, loadSettingsFromFile or loadSettingsFromDictionary")

        await self.setup.setup(address, sphereId, crownstoneId, meshDeviceKey, ibeaconUUID, ibeaconMajor, ibeaconMinor)

    async def disconnect(self):
        await self.ble.disconnect()
    
    async def startScanning(self, scanDuration=3):
        await self.ble.scan(scanDuration)

    async def stopScanning(self):
        await self.ble.stopScanning()


    async def getCrownstonesByScanning(self, scanDuration=3):
        gatherer = Gatherer()
        subscriptionIdAll = BleEventBus.subscribe(BleTopics.rawAdvertisement, lambda scanData: gatherer.handleAdvertisement(scanData))
        await self.ble.scan(duration=scanDuration)
        BleEventBus.unsubscribe(subscriptionIdAll)
        return gatherer.getCollection()


    async def isCrownstoneInSetupMode(self, address, scanDuration=3, waitUntilInRequiredMode=False):
        _LOGGER.debug(f"isCrownstoneInSetupMode address={address} scanDuration={scanDuration} waitUntilInRequiredMode={waitUntilInRequiredMode}")
        checker = SetupChecker(address, waitUntilInRequiredMode)
        subscriptionId = BleEventBus.subscribe(BleTopics.advertisement, checker.handleAdvertisement)
        await self.ble.scan(duration=scanDuration)
        BleEventBus.unsubscribe(subscriptionId)
        return checker.getResult()


    async def isCrownstoneInNormalMode(self, address, scanDuration=3, waitUntilInRequiredMode=False):
        _LOGGER.debug(f"isCrownstoneInNormalMode address={address} scanDuration={scanDuration} waitUntilInRequiredMode={waitUntilInRequiredMode}")
        checker = NormalModeChecker(address, waitUntilInRequiredMode)
        subscriptionId = BleEventBus.subscribe(BleTopics.rawAdvertisement, lambda scanData: checker.handleAdvertisement(scanData))
        await self.ble.scan(duration=scanDuration)
        BleEventBus.unsubscribe(subscriptionId)
        return checker.getResult()


    async def getRssiAverage(self, address, scanDuration=3):
        checker = RssiChecker(address)
        subscriptionId = BleEventBus.subscribe(BleTopics.rawAdvertisement, lambda scanData: checker.handleAdvertisement(scanData))
        await self.ble.scan(duration=scanDuration)
        BleEventBus.unsubscribe(subscriptionId)
        return checker.getResult()


    async def getNearestCrownstone(self, rssiAtLeast=-100, scanDuration=3, returnFirstAcceptable=False, addressesToExclude=None) -> ScanData or None:
        return self._getNearest(False, rssiAtLeast, scanDuration, returnFirstAcceptable, False, addressesToExclude)
    
    
    async def getNearestValidatedCrownstone(self, rssiAtLeast=-100, scanDuration=3, returnFirstAcceptable=False, addressesToExclude=None) -> ScanData or None:
        return self._getNearest(False, rssiAtLeast, scanDuration, returnFirstAcceptable, True, addressesToExclude)
    
    
    async def getNearestSetupCrownstone(self, rssiAtLeast=-100, scanDuration=3, returnFirstAcceptable=False, addressesToExclude=None) -> ScanData or None:
        return self._getNearest(True, rssiAtLeast, scanDuration, returnFirstAcceptable, True, addressesToExclude)


    async def _getNearest(self, setup, rssiAtLeast, scanDuration, returnFirstAcceptable, validated, addressesToExclude) -> ScanData or None:
        addressesToExcludeSet = set()
        if addressesToExclude is not None:
            for data in addressesToExclude:
                if hasattr(data,'address'):
                    addressesToExcludeSet.add(data.address.lower())
                elif isinstance(data, dict):
                    if "address" in data:
                        addressesToExcludeSet.add(data["address"].lower())
                    else:
                        raise CrownstoneException(CrownstoneError.INVALID_ADDRESS, "Addresses to Exclude is either an array of addresses (like 'f7:19:a4:ef:ea:f6') or an array of dicts with the field 'address'")
                else:
                    addressesToExcludeSet.add(data.lower())

        selector = NearestSelector(setup, rssiAtLeast, returnFirstAcceptable, addressesToExcludeSet)

        topic = BleTopics.advertisement
        if not validated:
            topic = BleTopics.rawAdvertisement

        subscriptionId = BleEventBus.subscribe(topic, lambda scanData: selector.handleAdvertisement(scanData))

        await self.ble.scan(duration=scanDuration)
    
        BleEventBus.unsubscribe(subscriptionId)
        
        return selector.getNearest()
