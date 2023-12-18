from enum import Enum
from typing import Dict

from simulator.units.si_prefixes import Prefix


class UnknownUnit(Exception):
	pass


class BasicUnit(Enum):
	NONE = None
	POSITION = "m"
	TIME = "s"
	AMOUNT_OF_SUBSTANCE = "mol"
	ELECTRIC_CURRENT = "A"
	TEMPERATURE = "K"
	LUMINOUS_INTENSITY = "cd"
	MASS = "g"


class UnitVector:
	def __init__(self, units: Dict):
		if not is_units_dict_valid(units):
			raise Exception("invalid dict with units")
		self.units = dict()
		self.is_none = True
		for basic_unit in BASIC_UNITS:
			if basic_unit not in units:
				self.units[basic_unit] = 0
			else:
				self.units[basic_unit] = units[basic_unit]
			if self.units[basic_unit] != 0:
				self.is_none = False

	def __add__(self, units):
		new_units = dict()
		if not is_units_dict_complete_and_valid(self.units) or not is_units_dict_complete_and_valid(units):
			raise Exception("units are not valid")
		for basic_unit in BASIC_UNITS:
			new_units = self.units[basic_unit] + units[basic_unit]
		return new_units

	def __radd__(self, units):
		new_units = dict()
		if not is_units_dict_complete_and_valid(units) or not is_units_dict_complete_and_valid(self.units):
			raise Exception("units are not valid")
		for basic_unit in BASIC_UNITS:
			new_units = units[basic_unit] + self.units[basic_unit]
		return new_units

	def __sub__(self, units):
		new_units = dict()
		if not is_units_dict_complete_and_valid(self.units) or not is_units_dict_complete_and_valid(units):
			raise Exception("units are not valid")
		for basic_unit in BASIC_UNITS:
			new_units = self.units[basic_unit] - units[basic_unit]
		return new_units

	def __rsub__(self, units):
		new_units = dict()
		if not is_units_dict_complete_and_valid(units) or not is_units_dict_complete_and_valid(self.units):
			raise Exception("units are not valid")
		for basic_unit in BASIC_UNITS:
			new_units = units[basic_unit] - self.units[basic_unit]
		return new_units

	def __eq__(self, units):
		if not is_units_dict_complete_and_valid(units) or not is_units_dict_complete_and_valid(self.units):
			raise Exception("units are not valid")
		for basic_unit in BASIC_UNITS:
			if units[basic_unit] != self.units[basic_unit]:
				return False
		return True


BASIC_UNITS = [BasicUnit.POSITION, BasicUnit.TIME, BasicUnit.AMOUNT_OF_SUBSTANCE, BasicUnit.ELECTRIC_CURRENT,
			   BasicUnit.TEMPERATURE, BasicUnit.LUMINOUS_INTENSITY, BasicUnit.MASS]


def is_units_dict_valid(units: Dict):
	for key in units.keys():
		if key not in BASIC_UNITS:
			return False
	return True


def is_units_dict_complete(units: Dict):
	for key in BASIC_UNITS:
		if key not in units:
			return False
	return True


def is_units_dict_complete_and_valid(units: Dict):
	return is_units_dict_complete(units) and is_units_dict_valid(units)


def complete_units_dict(units: Dict):
	for key in BASIC_UNITS:
		if key not in units:
			units[key] = 0


BASIC_UNIT_TO_STR = {
	BasicUnit.NONE: "",
	BasicUnit.POSITION: "m",
	BasicUnit.TIME: "s",
	BasicUnit.AMOUNT_OF_SUBSTANCE: "mol",
	BasicUnit.ELECTRIC_CURRENT: "A",
	BasicUnit.TEMPERATURE: "K",
	BasicUnit.LUMINOUS_INTENSITY: "cd",
	BasicUnit.MASS: "g"
}

BASIC_UNIT_TO_SI_PREFIX = {
	BasicUnit.NONE: Prefix.NONE,
	BasicUnit.POSITION: Prefix.STANDARD,
	BasicUnit.TIME: Prefix.STANDARD,
	BasicUnit.AMOUNT_OF_SUBSTANCE: Prefix.STANDARD,
	BasicUnit.ELECTRIC_CURRENT: Prefix.STANDARD,
	BasicUnit.TEMPERATURE: Prefix.STANDARD,
	BasicUnit.LUMINOUS_INTENSITY: Prefix.STANDARD,
	BasicUnit.MASS: Prefix.KILO
}
