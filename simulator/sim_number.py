from simulator.si_units.si_converter import convert_with_precision
from simulator.si_units.si_prefixes import Prefix, return_smaller_prefix, floor_prefix, SMALLEST_PREFIX, PREFIX_TO_STR
from .config.config import HIGH_PRECISION_WARNINGS, HIGH_PRECISION_DEBUGGING
import logging
import traceback


def __check_if_division_is_implemented(object_1, object_2):
	object_1_type = type(object_1)
	object_2_type = type(object_2)
	if object_1_type is not SimNumber and object_2_type is not SimNumber:
		logging.error("Trying to make an operation without a Sim number")
		raise NotImplemented

	if object_1_type is not SimNumber:
		object_temp = object_1
		object_temp_type = object_1_type

		object_1 = object_2
		object_1_type = object_2_type

		object_2 = object_temp
		object_2_type = object_temp_type

	if object_2_type is SimNumber:
		return

	if object_2_type is int:
		return

	raise NotImplemented


class SimNumber:
	def __init__(self, number=0, prefix=Prefix.NONE):
		if type(number) is float and prefix == Prefix.NONE:
			new_number = number
			exp = 0
			while new_number != int(new_number):
				new_number *= 10
				exp -= 1
			prefix = floor_prefix(exp)
			number = int(new_number)
		if type(number) is not int and HIGH_PRECISION_WARNINGS:
			logging.warning("Careful!!! Given number is a %s and not an int.", type(number))
			if HIGH_PRECISION_DEBUGGING:
				logging.debug("Number: %s StackTrace: ", number)
				logging.debug("".join(traceback.format_list(traceback.extract_stack())))
		self.__number = convert_with_precision(number, prefix, SMALLEST_PREFIX)
		self.current_prefix = prefix
		self.sim_prefix = SMALLEST_PREFIX

	def get_number(self):
		return convert_with_precision(self.__number, self.sim_prefix, self.current_prefix)

	def get_prefix(self):
		return self.current_prefix

	def get_sim_number(self):
		return self.__number

	def convert(self, target_prefix: Prefix):
		self.current_prefix = target_prefix
		return self

	def __add__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		return SimNumber(self.__number + number.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __radd__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		return SimNumber(number.__number + self.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __sub__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		return SimNumber(self.__number - number.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __rsub__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		return SimNumber(number.__number - self.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __mul__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		return SimNumber(self.__number * number.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __rmul__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		return SimNumber(number.__number * self.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __floordiv__(self, number):
		if type(number) is SimNumber:
			return SimNumber(self.__number // number.__number, SMALLEST_PREFIX).convert(
				return_smaller_prefix_between_sim_numbers(self, number))
		if type(number) is int:
			return SimNumber(self.__number // number, SMALLEST_PREFIX)
		raise NotImplemented

	def __rfloordiv__(self, number):
		if type(number) is not SimNumber:
			if type(number) is not int:
				raise NotImplemented
			return SimNumber(self.__number // number, SMALLEST_PREFIX)
		return SimNumber(number.__number // self.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __mod__(self, number):
		if type(number) is not SimNumber:
			if type(number) is not int:
				raise NotImplemented
			return SimNumber(self.__number % number, SMALLEST_PREFIX)
		return SimNumber(self.__number % number.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __rmod__(self, number):
		if type(number) is not SimNumber:
			if type(number) is not int:
				raise NotImplemented
			return SimNumber(self.__number % number, SMALLEST_PREFIX)
		return SimNumber(number.__number % self.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __divmod__(self, number):
		return self.__floordiv__(number), self.__mod__(number)

	def __rdivmod__(self, number):
		return self.__rfloordiv__(number), self.__rmod__(number)

	def __truediv__(self, number):
		if type(number) is not SimNumber:
			if type(number) is not int:
				raise NotImplemented
			return SimNumber(self.__number / number, SMALLEST_PREFIX)
		return SimNumber(self.__number / number.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __rtruediv__(self, number):
		if type(number) is not SimNumber:
			if type(number) is not int:
				raise NotImplemented
			return SimNumber(self.__number / number, SMALLEST_PREFIX)
		return SimNumber(number.__number / self.__number, SMALLEST_PREFIX).convert(
			return_smaller_prefix_between_sim_numbers(self, number))

	def __eq__(self, number):
		if type(number) is SimNumber:
			return (self.__number == number.__number and
					self.current_prefix == number.current_prefix and
					self.sim_prefix == number.sim_prefix)
		if type(number) is int:
			return self.__number == number
		return False

	def __bool__(self):
		return bool(self.__number)

	def __str__(self):
		return str(self.get_number()) + PREFIX_TO_STR[self.current_prefix]


def return_smaller_prefix_between_sim_numbers(sim_number1: SimNumber, sim_number2: SimNumber):
	# If they are the same, return one of them, doesn't matter
	if sim_number1.get_prefix() == sim_number2.get_prefix():
		return sim_number1.get_prefix()
	# If the first is None, return the second one
	elif sim_number1.get_prefix() == Prefix.NONE:
		return sim_number2.get_prefix()
	# If the second is None, return the first one
	elif sim_number2.get_prefix() == Prefix.NONE:
		return sim_number1.get_prefix()
	# Else return the smaller
	return return_smaller_prefix(sim_number1.current_prefix, sim_number2.current_prefix)
