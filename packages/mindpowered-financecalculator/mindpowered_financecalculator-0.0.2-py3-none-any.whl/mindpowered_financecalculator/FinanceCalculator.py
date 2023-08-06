import maglev
import financecalculator

from typing import Any, List, Callable

class FinanceCalculator:
	"""
	A library for performing various finance calculations
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = financecalculator.financecalculator_FinanceCalculator(bus)

	def PresentValueOfFutureMoney(self, futureValue: float, numPeriods: float, interestRate: float) -> object:
		"""		Calculate present value of future money
		Args:
			futureValue (float):Future Value
			numPeriods (float):Number of Periods
			interestRate (float):Interest Rate
		Returns:
			object containing Present Value and Total Interest
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [futureValue, numPeriods, interestRate]
		ret = None
		def PresentValueOfFutureMoney_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('FinanceCalculator.PresentValueOfFutureMoney', args, PresentValueOfFutureMoney_Ret)
		return ret

	def PresentValueOfDeposits(self, numPeriods: float, interestRate: float, depositAmount: float, depositAtBeginning: bool) -> object:
		"""		Calculate the present value of future deposits
		Args:
			numPeriods (float):Number of Periods
			interestRate (float):Interest Rate
			depositAmount (float):Periodic Deposit Amount
			depositAtBeginning (bool):Periodic Deposits made at beginning of period
		Returns:
			object containing Present Value, Total Principal, and Total Interest
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [numPeriods, interestRate, depositAmount, depositAtBeginning]
		ret = None
		def PresentValueOfDeposits_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('FinanceCalculator.PresentValueOfDeposits', args, PresentValueOfDeposits_Ret)
		return ret

	def FutureValue(self, presentValue: float, numPeriods: float, interestRate: float, timesCompoundedPerPeriod: float, depositAmount: float, depositAtBeginning: bool) -> object:
		"""		Calculate the future value of money and/or deposits
		Args:
			presentValue (float):Present Value
			numPeriods (float):Number of Periods
			interestRate (float):Interest rate as a percentage
			timesCompoundedPerPeriod (float):Times interest is compounded per period
			depositAmount (float):Periodic Deposit Amount
			depositAtBeginning (bool):Periodic Deposits made at beginning of period
		Returns:
			object containing Future Value and Total Interest
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [presentValue, numPeriods, interestRate, timesCompoundedPerPeriod, depositAmount, depositAtBeginning]
		ret = None
		def FutureValue_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('FinanceCalculator.FutureValue', args, FutureValue_Ret)
		return ret

	def NetPresentValue(self, initialInvestment: float, discountRate: float, timesCompoundedPerPeriod: float, cashFlowsAtBeginning: float, cashFlow: List[Any]) -> float:
		"""		Calculate net present value
		Args:
			initialInvestment (float):Initial Investment
			discountRate (float):Discount Rate (eg. Interest Rate)
			timesCompoundedPerPeriod (float):Times discount/interest is compounded per period
			cashFlowsAtBeginning (float):
			cashFlow (List[Any]):List of cash flows per period
		Returns:
			Net Present Value
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [initialInvestment, discountRate, timesCompoundedPerPeriod, cashFlowsAtBeginning, cashFlow]
		ret = None
		def NetPresentValue_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('FinanceCalculator.NetPresentValue', args, NetPresentValue_Ret)
		return ret



