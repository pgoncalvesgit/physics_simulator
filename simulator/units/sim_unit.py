from typing import Dict

from simulator.units.si_prefixes import Prefix
from simulator.units.sim_number import SimNumber
from simulator.units.units import BasicUnit, BASIC_UNIT_TO_STR, BASIC_UNITS, is_units_dict_valid, UnitVector


class OperationOnUnitNotAllowed(Exception):
	pass


class SimUnit(SimNumber):

	def __init__(self, number: SimNumber, units: UnitVector):
		super().__init__(number, number.get_prefix())
		self.units = units

	def __same_units_as(self, sim_unit):
		for basic_unit in BASIC_UNITS:
			if self.units[basic_unit] != sim_unit.units[basic_unit]:
				return False
		return True

	def __check_if_can_add_or_sub(self, number):
		if type(number) is not SimUnit and not self.units.is_none:
			raise OperationOnUnitNotAllowed
		if type(number) is SimUnit and self.__same_units_as(number):
			raise OperationOnUnitNotAllowed

	def __check_if_can_mult_or_div(self, number):
		if type(number) is SimUnit:
			# Either both are NONE or neither is NONE
			if self.units.is_none != number.is_none:
				raise OperationOnUnitNotAllowed

	def __add__(self, number):
		self.__check_if_can_add_or_sub(number)
		return SimUnit(super().__add__(number), self.units)

	def __radd__(self, number):
		self.__check_if_can_add_or_sub(number)
		return SimUnit(super().__radd__(number), self.units)

	def __sub__(self, number):
		self.__check_if_can_add_or_sub(number)
		return SimUnit(super().__sub__(number), self.units)

	def __rsub__(self, number):
		self.__check_if_can_add_or_sub(number)
		return SimUnit(super().__rsub__(number), self.units)

	def __mul__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units + number.units
		else:
			result_units = self.units
		return SimUnit(super().__mul__(number), result_units)

	def __rmul__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units + number.units
		else:
			result_units = self.units
		return SimUnit(super().__rmul__(number), result_units)

	def __floordiv__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units - number.units
		else:
			result_units = self.units
		return SimUnit(super().__floordiv__(number), result_units)

	def __rfloordiv__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units - number.units
		else:
			result_units = self.units
		return SimUnit(super().__rfloordiv__(number), result_units)

	def __mod__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units - number.units
		else:
			result_units = self.units
		return SimUnit(super().__mod__(number), result_units)

	def __rmod__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units - number.units
		else:
			result_units = self.units
		return SimUnit(super().__rmod__(number), result_units)

	def __divmod__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units - number.units
		else:
			result_units = self.units
		return SimUnit(super().__divmod__(number), result_units)

	def __rdivmod__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units - number.units
		else:
			result_units = self.units
		return SimUnit(super().__rdivmod__(number), result_units)

	def __truediv__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units - number.units
		else:
			result_units = self.units
		return SimUnit(super().__truediv__(number), result_units)

	def __rtruediv__(self, number):
		self.__check_if_can_mult_or_div(number)
		result_units: UnitVector
		if number is SimUnit:
			result_units = self.units - number.units
		else:
			result_units = self.units
		return SimUnit(super().__rtruediv__(number), result_units)

	def __eq__(self, number):
		if not super().__eq__(number):
			return False
		if type(number) is SimNumber and type(number) is not SimUnit:
			return self.units.is_none
		elif type(number) is SimUnit:
			return self.units == number.units
		elif type(number) is int:
			return not self.units.is_none
		raise NotImplementedError

	def __bool__(self):
		return super().__bool__()

	def __str__(self):
		return super().__str__() + str(self.units)
