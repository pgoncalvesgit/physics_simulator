from simulator.units.si_converter import convert_with_precision
from simulator.units.si_prefixes import Prefix, return_smaller_prefix, floor_prefix, \
	SMALLEST_PREFIX, PREFIX_TO_STR, PREFIX_TO_EXP
from .config.config import HIGH_PRECISION_WARNINGS, HIGH_PRECISION_DEBUGGING
import logging
import traceback


def __check_if_object_type_is_supported__(object_2):
	object_2_type = type(object_2)

	if object_2_type is SimNumber:
		return

	if object_2_type is int:
		return

	raise NotImplementedError


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

	def get_unsafe_number(self):
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
		result_sim_number = SimNumber(self.__number + number.__number, SMALLEST_PREFIX)
		result_sim_number.convert(return_smaller_prefix_between_sim_numbers(self, number))
		return result_sim_number

	def __radd__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		result_sim_number = SimNumber(number.__number + self.__number, SMALLEST_PREFIX)
		result_sim_number.convert(return_smaller_prefix_between_sim_numbers(number, self))
		return result_sim_number

	def __sub__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		result_sim_number = SimNumber(self.__number - number.__number, SMALLEST_PREFIX)
		result_sim_number.convert(return_smaller_prefix_between_sim_numbers(self, number))
		return result_sim_number

	def __rsub__(self, number):
		if type(number) is not SimNumber:
			number = SimNumber(number)
		result_sim_number = SimNumber(number.__number - self.__number, SMALLEST_PREFIX)
		result_sim_number.convert(return_smaller_prefix_between_sim_numbers(number, self))
		return result_sim_number

	def __mul__(self, number):
		result_sim_number: SimNumber
		__check_if_object_type_is_supported__(number)
		if type(number) is int:
			result_sim_number = SimNumber(self.__number * number, SMALLEST_PREFIX)
			result_sim_number.convert(self.get_prefix())
		# When multiplying, if we have 2 * 2 the simulator thinks its 20...00 * 20...00
		# This will create a new number 40...00 with 2n zeros
		# It needs to know that when multiplying two sim numbers,
		# we will need to remove the "smallest exp last digits"
		# For example, if the smallest exp is 1e-30, we need to remove 30 digits
		elif type(number) is SimNumber:
			result_sim_number = SimNumber(self.__number * number.__number, SMALLEST_PREFIX)
			for i in range(0, PREFIX_TO_EXP[SMALLEST_PREFIX] + 1, -1):
				result_sim_number.__number = result_sim_number.__number // 10
			# TODO: Adjust with the even/odd rule
			if result_sim_number.__number % 10 >= 5:
				result_sim_number.__number = result_sim_number.__number // 10 + 1
			else:
				result_sim_number.__number = result_sim_number.__number // 10
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(self, number))
		# TODO: support units (mass, time, position, etc...)
		else:
			raise NotImplementedError
		return result_sim_number

	def __rmul__(self, number):
		result_sim_number: SimNumber
		__check_if_object_type_is_supported__(number)
		if type(number) is int:
			result_sim_number = SimNumber(number * self.__number, SMALLEST_PREFIX)
			result_sim_number.convert(self.get_prefix())
		# When multiplying, if we have 2 * 2 the simulator thinks its 20...00 * 20...00
		# This will create a new number 40...00 with 2n zeros
		# It needs to know that when multiplying two sim numbers,
		# we will need to remove the "smallest exp last digits"
		# For example, if the smallest exp is 1e-30, we need to remove 30 digits
		elif type(number) is SimNumber:
			result_sim_number = SimNumber(number.__number * self.__number, SMALLEST_PREFIX)
			for i in range(0, PREFIX_TO_EXP[SMALLEST_PREFIX] + 1, -1):
				result_sim_number.__number = result_sim_number.__number // 10
			# TODO: Adjust with the even/odd rule
			if result_sim_number.__number % 10 >= 5:
				result_sim_number.__number = result_sim_number.__number // 10 + 1
			else:
				result_sim_number.__number = result_sim_number.__number // 10 + 1
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(number, self))
		# TODO: support units (mass, time, position, etc...)
		else:
			raise NotImplementedError
		return result_sim_number

	def __floordiv__(self, number):
		result_sim_number: SimNumber
		__check_if_object_type_is_supported__(number)
		if type(number) is int:
			result_sim_number = SimNumber(self.__number // number, SMALLEST_PREFIX)
			result_sim_number.convert(self.get_prefix())
		# When dividing, if we have 2 / 2 the simulator thinks its 20...00 / 20...00
		# This will create a new number 1 with no zeros
		# It needs to know that when dividing two sim numbers,
		# we will need to add the "smallest exp last digits"
		# For example, if the smallest exp is 1e-30, we need to add 30 digits
		elif type(number) is SimNumber:
			result_sim_number = SimNumber(self.__number // number.__number, SMALLEST_PREFIX)
			for i in range(0, PREFIX_TO_EXP[SMALLEST_PREFIX], -1):
				result_sim_number.__number = result_sim_number.__number * 10
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(self, number))
		# TODO: support units (mass, time, position, etc...)
		else:
			raise NotImplementedError
		return result_sim_number

	def __rfloordiv__(self, number):
		result_sim_number: SimNumber
		__check_if_object_type_is_supported__(number)
		if type(number) is int:
			result_sim_number = SimNumber(number // self.__number, SMALLEST_PREFIX)
			result_sim_number.convert(self.get_prefix())
		# When dividing, if we have 2 / 2 the simulator thinks its 20...00 / 20...00
		# This will create a new number 1 with no zeros
		# It needs to know that when dividing two sim numbers,
		# we will need to add the "smallest exp last digits"
		# For example, if the smallest exp is 1e-30, we need to add 30 digits
		elif type(number) is SimNumber:
			result_sim_number = SimNumber(number.__number // self.__number, SMALLEST_PREFIX)
			for i in range(0, PREFIX_TO_EXP[SMALLEST_PREFIX], -1):
				result_sim_number.__number = result_sim_number.__number * 10
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(number, self))
		# TODO: support units (mass, time, position, etc...)
		else:
			raise NotImplementedError
		return result_sim_number

	def __mod__(self, number):
		result_sim_number: SimNumber
		__check_if_object_type_is_supported__(number)
		if type(number) is int:
			result_sim_number = SimNumber(self.__number % number, SMALLEST_PREFIX)
			for i in range(0, PREFIX_TO_EXP[SMALLEST_PREFIX], -1):
				result_sim_number.__number = result_sim_number.__number * 10
			result_sim_number.convert(self.get_prefix())
		elif type(number) is SimNumber:
			result_sim_number = SimNumber(self.__number % number.__number, SMALLEST_PREFIX)
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(self, number))
		# TODO: support units (mass, time, position, etc...)
		else:
			raise NotImplementedError
		return result_sim_number

	def __rmod__(self, number):
		result_sim_number: SimNumber
		__check_if_object_type_is_supported__(number)
		if type(number) is int:
			result_sim_number = SimNumber(number % self.__number, SMALLEST_PREFIX)
			for i in range(0, PREFIX_TO_EXP[SMALLEST_PREFIX], -1):
				result_sim_number.__number = result_sim_number.__number * 10
			result_sim_number.convert(self.get_prefix())
		elif type(number) is SimNumber:
			result_sim_number = SimNumber(number.__number % self.__number, SMALLEST_PREFIX)
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(number, self))
		# TODO: support units (mass, time, position, etc...)
		else:
			raise NotImplementedError
		return result_sim_number

	def __divmod__(self, number):
		return self.__floordiv__(number), self.__mod__(number)

	def __rdivmod__(self, number):
		return self.__rfloordiv__(number), self.__rmod__(number)

	def __truediv__(self, number):
		result_sim_number: SimNumber
		__check_if_object_type_is_supported__(number)
		if type(number) is int:
			result_sim_number = SimNumber(self.__number // number, SMALLEST_PREFIX)
			result_sim_number.convert(self.get_prefix())
		elif type(number) is SimNumber:
			current_exp = PREFIX_TO_EXP[SMALLEST_PREFIX] + 1
			final_number = self.__number // number.__number
			current_normalized_remainer = self.__number % number.__number * 10
			while current_exp <= 0 and current_normalized_remainer != 0:
				value_to_add = current_normalized_remainer // number.__number
				current_normalized_remainer = current_normalized_remainer % number.__number * 10
				final_number = final_number * 10 + value_to_add
				current_exp += 1
			while current_exp <= 0:
				final_number *= 10
				current_exp += 1

			result_sim_number = SimNumber(final_number, SMALLEST_PREFIX)
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(self, number))
		# TODO: support units (mass, time, position, etc...)
		else:
			raise NotImplementedError
		return result_sim_number

	def __rtruediv__(self, number):
		result_sim_number: SimNumber
		__check_if_object_type_is_supported__(number)
		if type(number) is int:
			number = SimNumber(number)
			current_exp = PREFIX_TO_EXP[SMALLEST_PREFIX] + 1
			final_number = number.__number // self.__number
			current_normalized_remainer = number.__number % self.__number * 10
			while current_exp <= 0 and current_normalized_remainer != 0:
				value_to_add = current_normalized_remainer // self.__number
				current_normalized_remainer = current_normalized_remainer % self.__number * 10
				final_number = final_number * 10 + value_to_add
				current_exp += 1
			while current_exp <= 0:
				final_number *= 10
				current_exp += 1

			result_sim_number = SimNumber(final_number, SMALLEST_PREFIX)
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(number, self))
		elif type(number) is SimNumber:
			current_exp = PREFIX_TO_EXP[SMALLEST_PREFIX] + 1
			final_number = number.__number // self.__number
			current_normalized_remainer = number.__number % self.__number * 10
			while current_exp <= 0 and current_normalized_remainer != 0:
				value_to_add = current_normalized_remainer // self.__number
				current_normalized_remainer = current_normalized_remainer % self.__number * 10
				final_number = final_number * 10 + value_to_add
				current_exp += 1
			while current_exp <= 0:
				final_number *= 10
				current_exp += 1

			result_sim_number = SimNumber(final_number, SMALLEST_PREFIX)
			# TODO: Prefix may need to change. 2g * 0.5 -> ????
			result_sim_number.convert(return_smaller_prefix_between_sim_numbers(number, self))
		# TODO: support units (mass, time, position, etc...)
		else:
			raise NotImplementedError
		return result_sim_number

	def __eq__(self, number):
		if type(number) is SimNumber:
			return (self.__number == number.__number and
					self.current_prefix == number.current_prefix and
					self.sim_prefix == number.sim_prefix)
		if type(number) is int and self.get_prefix() == Prefix.NONE:
			return self.get_unsafe_number() == number
		return False

	def __bool__(self):
		return bool(self.__number)

	def __str__(self):
		return str(self.get_unsafe_number()) + PREFIX_TO_STR[self.current_prefix]


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
