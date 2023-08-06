from crownstone_core.Exceptions import CrownstoneError, CrownstoneException
from crownstone_core.packets.ResultPacket import ResultPacket
from crownstone_core.packets.debug.AdcChannelSwapsPacket import AdcChannelSwapsPacket
from crownstone_core.packets.debug.AdcRestartsPacket import AdcRestartsPacket
from crownstone_core.packets.debug.PowerSamplesPacket import PowerSamplesPacket
from crownstone_core.packets.debug.SwitchHistoryPacket import SwitchHistoryListPacket
from crownstone_core.protocol.BluenetTypes import ResultValue
from crownstone_core.protocol.Characteristics import CrownstoneCharacteristics
from crownstone_core.protocol.ControlPackets import ControlPacket, ControlType
from crownstone_core.protocol.ControlPackets import ControlPacketsGenerator
from crownstone_core.protocol.Services import CSServices
from crownstone_core.util.Conversion import Conversion


class DebugHandler:
	def __init__(self, bluetoothCore):
		self.core = bluetoothCore

	async def getUptime(self):
		""" Get the uptime of the crownstone in seconds. """
		controlPacket = ControlPacket(ControlType.GET_UPTIME).getPacket()
		result = await self._writeControlAndGetResult(controlPacket)
		if result.resultCode != ResultValue.SUCCESS:
			raise CrownstoneException(CrownstoneError.RESULT_NOT_SUCCESS, "Result: " + str(result.resultCode))
		return Conversion.uint8_array_to_uint32(result.payload)

	async def getAdcRestarts(self):
		"""	Get number of ADC restarts since boot. Returns an AdcRestartsPacket. """
		controlPacket = ControlPacket(ControlType.GET_ADC_RESTARTS).getPacket()
		result = await self._writeControlAndGetResult(controlPacket)
		if result.resultCode != ResultValue.SUCCESS:
			raise CrownstoneException(CrownstoneError.RESULT_NOT_SUCCESS, "Result: " + str(result.resultCode))
		return AdcRestartsPacket(result.payload)

	async def getAdcChannelSwaps(self):
		""" Get number of ADC channel swaps since boot. Returns an AdcChannelSwapsPacket. """
		controlPacket = ControlPacket(ControlType.GET_ADC_CHANNEL_SWAPS).getPacket()
		result = await self._writeControlAndGetResult(controlPacket)
		if result.resultCode != ResultValue.SUCCESS:
			raise CrownstoneException(CrownstoneError.RESULT_NOT_SUCCESS, "Result: " + str(result.resultCode))
		return AdcChannelSwapsPacket(result.payload)

	async def getSwitchHistory(self):
		""" Get the switch history. Returns a SwitchHistoryListPacket. """
		controlPacket = ControlPacket(ControlType.GET_SWITCH_HISTORY).getPacket()
		result = await self._writeControlAndGetResult(controlPacket)
		if result.resultCode != ResultValue.SUCCESS:
			raise CrownstoneException(CrownstoneError.RESULT_NOT_SUCCESS, "Result: " + str(result.resultCode))
		return SwitchHistoryListPacket(result.payload)

	async def getPowerSamples(self, samplesType):
		""" Get all power samples of the given type. Returns a list of PowerSamplesPacket. """
		allSamples = []
		index = 0
		while True:
			result = await self._getPowerSamples(samplesType, index)
			if result.resultCode == ResultValue.WRONG_PARAMETER:
				return allSamples
			elif result.resultCode == ResultValue.SUCCESS:
				samples = PowerSamplesPacket(result.payload)
				allSamples.append(samples)
				index += 1
			else:
				raise CrownstoneException(CrownstoneError.RESULT_NOT_SUCCESS, "Result: " + str(result.resultCode))

	async def getPowerSamplesAtIndex(self, samplesType, index):
		""" Get power samples of given type at given index. Returns a PowerSamplesPacket. """
		result = await self._getPowerSamples(samplesType, index)
		if result.resultCode != ResultValue.SUCCESS:
			raise CrownstoneException(CrownstoneError.RESULT_NOT_SUCCESS, "Result: " + str(result.resultCode))
		return PowerSamplesPacket(result.payload)

	async def _getPowerSamples(self, samplesType, index):
		""" Get power samples of given type at given index, but don't check result code. """
		controlPacket = ControlPacketsGenerator.getPowerSamplesRequestPacket(samplesType, index)
		return await self._writeControlAndGetResult(controlPacket)

	async def _writeControlPacket(self, packet):
		""" Write the control packet. """
		await self.core.ble.writeToCharacteristic(CSServices.CrownstoneService, CrownstoneCharacteristics.Control, packet)

	async def _writeControlAndGetResult(self, controlPacket):
		""" Writes the control packet, and returns the result packet. """
		result = await self.core.ble.setupSingleNotification(CSServices.CrownstoneService, CrownstoneCharacteristics.Result, lambda: self._writeControlPacket(controlPacket))
		resultPacket = ResultPacket(result)
		if not resultPacket.valid:
			raise CrownstoneException(CrownstoneError.INCORRECT_RESPONSE_LENGTH, "Result is invalid")
		return resultPacket
