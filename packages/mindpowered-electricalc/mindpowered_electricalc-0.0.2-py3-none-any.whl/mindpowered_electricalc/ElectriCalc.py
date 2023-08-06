import maglev
import electricalc

from typing import Any, List, Callable

class ElectriCalc:
	"""
	A library for calculations related to electrical wiring and circuits
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = electricalc.electricalc_ElectricalCalculator(bus)

	def ConvertPhaseAngleToPowerFactor(self, phaseAngle: float) -> float:
		"""		Convert from Phase Angle to Power Factor
		Args:
			phaseAngle (float):Phase Angle in degrees
		Returns:
			Power Factor
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [phaseAngle]
		ret = None
		def ConvertPhaseAngleToPowerFactor_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ElectriCalc.ConvertPhaseAngleToPowerFactor', args, ConvertPhaseAngleToPowerFactor_Ret)
		return ret

	def ConvertPowerFactorToPhaseAngle(self, powerFactor: float) -> float:
		"""		Convert from Power Factor to Phase Angle
		Args:
			powerFactor (float):Power Factor
		Returns:
			Phase Angle in degrees
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [powerFactor]
		ret = None
		def ConvertPowerFactorToPhaseAngle_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ElectriCalc.ConvertPowerFactorToPhaseAngle', args, ConvertPowerFactorToPhaseAngle_Ret)
		return ret

	def CalculateSinglePhasePower(self, voltage: float, current: float) -> float:
		"""		Calcualte single phase power based on measured voltage and current
		Args:
			voltage (float):Measured voltage in Volts
			current (float):Measured current in Amps
		Returns:
			Apparent Power in VA
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [voltage, current]
		ret = None
		def CalculateSinglePhasePower_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ElectriCalc.CalculateSinglePhasePower', args, CalculateSinglePhasePower_Ret)
		return ret

	def CalculateThreePhasePower(self, voltage: float, lineTo: str, current: float) -> float:
		"""		Calcualte three phase power based on measured voltage and current
		Args:
			voltage (float):Measured voltage in Volts
			lineTo (str):Which voltage was measured. Must be "line" or "netural"
			current (float):Measured current in Amps
		Returns:
			Apparent Power in VA
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [voltage, lineTo, current]
		ret = None
		def CalculateThreePhasePower_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ElectriCalc.CalculateThreePhasePower', args, CalculateThreePhasePower_Ret)
		return ret



