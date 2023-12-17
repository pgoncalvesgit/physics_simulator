import pytest

from ..sim_number import SimNumber
from ..units.si_prefixes import Prefix, PREFIX_TO_EXP, SMALLEST_PREFIX


class SimNumberTester():

	def __init__(self, sim_number: SimNumber):
		self.sim_number = sim_number
		self.first_digit_exponent = 0
		current_number = self.sim_number.get_sim_number()
		while current_number // 10 >= 1:
			self.first_digit_exponent += 1
			current_number //= 10

	def equals_division(self, numerator, denominator):
		number_to_test = self.sim_number.get_sim_number()
		current_numerator = numerator
		current_denominator = denominator

		current_exp = self.first_digit_exponent
		lowest_exp = PREFIX_TO_EXP[SMALLEST_PREFIX]
		if current_exp < 0:
			return False

		# current_exp = first_digit_exp - lowest_exp
		# if Lowest exp is 1, current exp will be first_digit_exp - 1
		# if Lowest exp is -30, current exp will be first_digit_exp - (-30)
		# Therefore, by adding them together, we get the exp for the true number
		# We want to shift the . to the first digit, so we do this
		first_digit_exp = current_exp + lowest_exp
		while first_digit_exp > 0:
			current_denominator *= 10
			first_digit_exp -= 1
		while first_digit_exp < 0:
			current_numerator *= 10
			first_digit_exp += 1

		while current_exp >= 0:
			# Get the digit being tested without floats
			temp_exp = current_exp
			digit_to_test = number_to_test
			while temp_exp > 0:
				digit_to_test //= 10
				temp_exp -= 1
			digit_to_test %= 10

			# Get the real digit to test without float shenanigans
			real_digit = current_numerator/current_denominator // 1
			if digit_to_test != real_digit:
				return False
			current_exp -= 1
			# The following line would remove the real digit, but we would be executing that on a float, which we do not want
			# 	current_numerator / current_denominator - real_digit
			# For that reason, we put it inside the numerator by multiplying by the denominator
			# We then multiply by 10 to get the next digit
			current_numerator = (current_numerator - real_digit*current_denominator) * 10
		return True


NUMBER1 = 54
NUMBER2 = 15

SIM_NUMBER_1_STD = SimNumber(NUMBER1, Prefix.STANDARD)
SIM_NUMBER_2_STD = SimNumber(NUMBER2, Prefix.STANDARD)

SIM_NUMBER_1_NONE = SimNumber(NUMBER1, Prefix.NONE)
SIM_NUMBER_2_NONE = SimNumber(NUMBER2, Prefix.NONE)

INT_NUMBER = 3
FLOAT_NUMBER = 6.023

MIN_ERROR = 1e-8


def test_add_operations():
	# check __add__
	assert (SIM_NUMBER_1_STD + SIM_NUMBER_2_STD).get_unsafe_number() == NUMBER1 + NUMBER2
	assert (SIM_NUMBER_2_STD + SIM_NUMBER_1_STD).get_unsafe_number() == NUMBER2 + NUMBER1
	assert (SIM_NUMBER_2_STD + SIM_NUMBER_1_STD).get_prefix() == Prefix.STANDARD

	assert (SIM_NUMBER_1_STD + SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 + NUMBER2
	assert (SIM_NUMBER_1_STD + SIM_NUMBER_2_NONE).get_prefix() == Prefix.STANDARD

	assert (SIM_NUMBER_2_STD + SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 + NUMBER1
	assert (SIM_NUMBER_2_STD + SIM_NUMBER_1_NONE).get_prefix() == Prefix.STANDARD

	assert (SIM_NUMBER_1_NONE + SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 + NUMBER2
	assert (SIM_NUMBER_1_NONE + SIM_NUMBER_2_NONE).get_prefix() == Prefix.NONE
	assert (SIM_NUMBER_2_NONE + SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 + NUMBER1
	assert (SIM_NUMBER_2_NONE + SIM_NUMBER_1_NONE).get_prefix() == Prefix.NONE

	assert (SIM_NUMBER_1_STD + INT_NUMBER).get_unsafe_number() == NUMBER1 + INT_NUMBER
	assert (SIM_NUMBER_1_STD + INT_NUMBER).get_prefix() == Prefix.STANDARD
	assert (SIM_NUMBER_2_STD + INT_NUMBER).get_unsafe_number() == NUMBER2 + INT_NUMBER
	assert (SIM_NUMBER_2_STD + INT_NUMBER).get_prefix() == Prefix.STANDARD

	# check __radd__
	assert (INT_NUMBER + SIM_NUMBER_1_STD).get_unsafe_number() == INT_NUMBER + NUMBER1
	assert (INT_NUMBER + SIM_NUMBER_1_STD).get_prefix() == Prefix.STANDARD

	assert (INT_NUMBER + SIM_NUMBER_1_NONE).get_unsafe_number() == INT_NUMBER + NUMBER1
	assert (INT_NUMBER + SIM_NUMBER_1_NONE).get_prefix() == Prefix.NONE

	assert (INT_NUMBER + SIM_NUMBER_2_STD).get_unsafe_number() == INT_NUMBER + NUMBER2
	assert (INT_NUMBER + SIM_NUMBER_2_STD).get_prefix() == Prefix.STANDARD

	assert (INT_NUMBER + SIM_NUMBER_2_NONE).get_unsafe_number() == INT_NUMBER + NUMBER2
	assert (INT_NUMBER + SIM_NUMBER_2_NONE).get_prefix() == Prefix.NONE


def test_sub_operations():
	# check __sub__
	assert (SIM_NUMBER_1_STD - SIM_NUMBER_2_STD).get_unsafe_number() == NUMBER1 - NUMBER2
	assert (SIM_NUMBER_2_STD - SIM_NUMBER_1_STD).get_unsafe_number() == NUMBER2 - NUMBER1
	assert (SIM_NUMBER_1_STD - SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 - NUMBER2
	assert (SIM_NUMBER_2_STD - SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 - NUMBER1
	assert (SIM_NUMBER_1_NONE - SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 - NUMBER2
	assert (SIM_NUMBER_2_NONE - SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 - NUMBER1
	assert (SIM_NUMBER_1_STD - INT_NUMBER).get_unsafe_number() == NUMBER1 - INT_NUMBER
	assert (SIM_NUMBER_2_STD - INT_NUMBER).get_unsafe_number() == NUMBER2 - INT_NUMBER

	# check __rsub__
	assert (INT_NUMBER - SIM_NUMBER_1_STD).get_unsafe_number() == INT_NUMBER - NUMBER1
	assert (INT_NUMBER - SIM_NUMBER_2_STD).get_unsafe_number() == INT_NUMBER - NUMBER2


def test_mul_operations():
	# check __mul__
	assert (SIM_NUMBER_1_STD * SIM_NUMBER_2_STD).get_unsafe_number() == NUMBER1 * NUMBER2
	assert (SIM_NUMBER_2_STD * SIM_NUMBER_1_STD).get_unsafe_number() == NUMBER2 * NUMBER1
	assert (SIM_NUMBER_1_STD * SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 * NUMBER2
	assert (SIM_NUMBER_2_STD * SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 * NUMBER1
	assert (SIM_NUMBER_1_NONE * SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 * NUMBER2
	assert (SIM_NUMBER_2_NONE * SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 * NUMBER1
	assert (SIM_NUMBER_1_STD * INT_NUMBER).get_unsafe_number() == NUMBER1 * INT_NUMBER
	assert (SIM_NUMBER_2_STD * INT_NUMBER).get_unsafe_number() == NUMBER2 * INT_NUMBER

	# check __rmul__
	assert (INT_NUMBER * SIM_NUMBER_1_STD).get_unsafe_number() == INT_NUMBER * NUMBER1
	assert (INT_NUMBER * SIM_NUMBER_2_STD).get_unsafe_number() == INT_NUMBER * NUMBER2


def test_floor_operations():
	# check __floor__
	assert (SIM_NUMBER_1_STD // SIM_NUMBER_2_STD).get_unsafe_number() == NUMBER1 // NUMBER2
	assert (SIM_NUMBER_2_STD // SIM_NUMBER_1_STD).get_unsafe_number() == NUMBER2 // NUMBER1
	assert (SIM_NUMBER_1_STD // SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 // NUMBER2
	assert (SIM_NUMBER_2_STD // SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 // NUMBER1
	assert (SIM_NUMBER_1_NONE // SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 // NUMBER2
	assert (SIM_NUMBER_2_NONE // SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 // NUMBER1
	assert (SIM_NUMBER_1_STD // INT_NUMBER).get_unsafe_number() == NUMBER1 // INT_NUMBER
	assert (SIM_NUMBER_2_STD // INT_NUMBER).get_unsafe_number() == NUMBER2 // INT_NUMBER

	# check __rfloor__
	assert (INT_NUMBER // SIM_NUMBER_1_STD).get_unsafe_number() == INT_NUMBER // NUMBER1
	assert (INT_NUMBER // SIM_NUMBER_2_STD).get_unsafe_number() == INT_NUMBER // NUMBER2


def test_mod_operations():
	# check __mod__
	assert (SIM_NUMBER_1_STD % SIM_NUMBER_2_STD).get_unsafe_number() == NUMBER1 % NUMBER2
	assert (SIM_NUMBER_2_STD % SIM_NUMBER_1_STD).get_unsafe_number() == NUMBER2 % NUMBER1
	assert (SIM_NUMBER_1_STD % SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 % NUMBER2
	assert (SIM_NUMBER_2_STD % SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 % NUMBER1
	assert (SIM_NUMBER_1_NONE % SIM_NUMBER_2_NONE).get_unsafe_number() == NUMBER1 % NUMBER2
	assert (SIM_NUMBER_2_NONE % SIM_NUMBER_1_NONE).get_unsafe_number() == NUMBER2 % NUMBER1
	assert (SIM_NUMBER_1_STD % INT_NUMBER).get_unsafe_number() == NUMBER1 % INT_NUMBER
	assert (SIM_NUMBER_2_STD % INT_NUMBER).get_unsafe_number() == NUMBER2 % INT_NUMBER

	# check __rmod__
	assert (INT_NUMBER % SIM_NUMBER_1_STD).get_unsafe_number() == INT_NUMBER % NUMBER1
	assert (INT_NUMBER % SIM_NUMBER_2_STD).get_unsafe_number() == INT_NUMBER % NUMBER2


# TODO
def test_divmod_operations():
	# check __divmod__
	assert divmod(SIM_NUMBER_1_STD, SIM_NUMBER_2_STD)[0].get_unsafe_number() == NUMBER1 // NUMBER2
	assert divmod(SIM_NUMBER_1_STD, SIM_NUMBER_2_STD)[1].get_unsafe_number() == NUMBER1 % NUMBER2
	assert divmod(SIM_NUMBER_2_STD, SIM_NUMBER_1_STD)[0].get_unsafe_number() == NUMBER2 // NUMBER1
	assert divmod(SIM_NUMBER_2_STD, SIM_NUMBER_1_STD)[1].get_unsafe_number() == NUMBER2 % NUMBER1

	assert divmod(SIM_NUMBER_1_STD, SIM_NUMBER_2_NONE)[0].get_unsafe_number() == NUMBER1 // NUMBER2
	assert divmod(SIM_NUMBER_1_STD, SIM_NUMBER_2_NONE)[1].get_unsafe_number() == NUMBER1 % NUMBER2
	assert divmod(SIM_NUMBER_2_STD, SIM_NUMBER_1_NONE)[0].get_unsafe_number() == NUMBER2 // NUMBER1
	assert divmod(SIM_NUMBER_2_STD, SIM_NUMBER_1_NONE)[1].get_unsafe_number() == NUMBER2 % NUMBER1
	assert divmod(SIM_NUMBER_1_NONE, SIM_NUMBER_2_NONE)[0].get_unsafe_number() == NUMBER1 // NUMBER2
	assert divmod(SIM_NUMBER_1_NONE, SIM_NUMBER_2_NONE)[1].get_unsafe_number() == NUMBER1 % NUMBER2
	assert divmod(SIM_NUMBER_2_NONE, SIM_NUMBER_1_NONE)[0].get_unsafe_number() == NUMBER2 // NUMBER1
	assert divmod(SIM_NUMBER_2_NONE, SIM_NUMBER_1_NONE)[1].get_unsafe_number() == NUMBER2 % NUMBER1

	assert divmod(SIM_NUMBER_1_STD, INT_NUMBER)[0].get_unsafe_number() == NUMBER1 // INT_NUMBER
	assert divmod(SIM_NUMBER_1_STD, INT_NUMBER)[1].get_unsafe_number() == NUMBER1 % INT_NUMBER
	assert divmod(SIM_NUMBER_2_STD, INT_NUMBER)[0].get_unsafe_number() == NUMBER2 // INT_NUMBER
	assert divmod(SIM_NUMBER_2_STD, INT_NUMBER)[1].get_unsafe_number() == NUMBER2 % INT_NUMBER
	assert divmod(SIM_NUMBER_1_NONE, INT_NUMBER)[0].get_unsafe_number() == NUMBER1 // INT_NUMBER
	assert divmod(SIM_NUMBER_1_NONE, INT_NUMBER)[1].get_unsafe_number() == NUMBER1 % INT_NUMBER
	assert divmod(SIM_NUMBER_2_NONE, INT_NUMBER)[0].get_unsafe_number() == NUMBER2 // INT_NUMBER
	assert divmod(SIM_NUMBER_2_NONE, INT_NUMBER)[1].get_unsafe_number() == NUMBER2 % INT_NUMBER

	# check __divmod__
	assert divmod(INT_NUMBER, SIM_NUMBER_1_STD)[0].get_unsafe_number() == INT_NUMBER // NUMBER1
	assert divmod(INT_NUMBER, SIM_NUMBER_1_STD)[1].get_unsafe_number() == INT_NUMBER % NUMBER1
	assert divmod(INT_NUMBER, SIM_NUMBER_1_NONE)[0].get_unsafe_number() == INT_NUMBER // NUMBER1
	assert divmod(INT_NUMBER, SIM_NUMBER_1_NONE)[1].get_unsafe_number() == INT_NUMBER % NUMBER1
	assert divmod(INT_NUMBER, SIM_NUMBER_2_STD)[0].get_unsafe_number() == INT_NUMBER // NUMBER2
	assert divmod(INT_NUMBER, SIM_NUMBER_2_STD)[1].get_unsafe_number() == INT_NUMBER % NUMBER2
	assert divmod(INT_NUMBER, SIM_NUMBER_2_NONE)[0].get_unsafe_number() == INT_NUMBER // NUMBER2
	assert divmod(INT_NUMBER, SIM_NUMBER_2_NONE)[1].get_unsafe_number() == INT_NUMBER % NUMBER2


def test_truediv_operations():
	# check __truediv__
	# TODO: This should result in a NONE or a really small number
	assert SimNumberTester(SIM_NUMBER_1_STD / SIM_NUMBER_1_NONE).equals_division(NUMBER1, NUMBER1)
	assert SimNumberTester(SIM_NUMBER_1_STD / SIM_NUMBER_1_STD).equals_division(NUMBER1, NUMBER1)
	assert SimNumberTester(SIM_NUMBER_1_STD / SIM_NUMBER_2_STD).equals_division(NUMBER1, NUMBER2)
	assert SimNumberTester(SIM_NUMBER_1_STD / SIM_NUMBER_2_NONE).equals_division(NUMBER1, NUMBER2)

	assert SimNumberTester(SIM_NUMBER_1_NONE / SIM_NUMBER_1_NONE).equals_division(NUMBER1, NUMBER1)
	assert SimNumberTester(SIM_NUMBER_1_NONE / SIM_NUMBER_1_STD).equals_division(NUMBER1, NUMBER1)
	assert SimNumberTester(SIM_NUMBER_1_NONE / SIM_NUMBER_2_STD).equals_division(NUMBER1, NUMBER2)
	assert SimNumberTester(SIM_NUMBER_1_NONE / SIM_NUMBER_2_NONE).equals_division(NUMBER1, NUMBER2)

	assert SimNumberTester(SIM_NUMBER_2_STD / SIM_NUMBER_1_NONE).equals_division(NUMBER2, NUMBER1)
	assert SimNumberTester(SIM_NUMBER_2_STD / SIM_NUMBER_1_STD).equals_division(NUMBER2, NUMBER1)
	assert SimNumberTester(SIM_NUMBER_2_STD / SIM_NUMBER_2_STD).equals_division(NUMBER2, NUMBER2)
	assert SimNumberTester(SIM_NUMBER_2_STD / SIM_NUMBER_2_NONE).equals_division(NUMBER2, NUMBER2)

	assert SimNumberTester(SIM_NUMBER_2_NONE / SIM_NUMBER_1_NONE).equals_division(NUMBER2, NUMBER1)
	assert SimNumberTester(SIM_NUMBER_2_NONE / SIM_NUMBER_1_STD).equals_division(NUMBER2, NUMBER1)
	assert SimNumberTester(SIM_NUMBER_2_NONE / SIM_NUMBER_2_STD).equals_division(NUMBER2, NUMBER2)
	assert SimNumberTester(SIM_NUMBER_2_NONE / SIM_NUMBER_2_NONE).equals_division(NUMBER2, NUMBER2)

	# check __rtruediv__
	assert SimNumberTester(INT_NUMBER / SIM_NUMBER_1_NONE).equals_division(INT_NUMBER, NUMBER1)
	assert SimNumberTester(INT_NUMBER / SIM_NUMBER_1_STD).equals_division(INT_NUMBER, NUMBER1)
	assert SimNumberTester(INT_NUMBER / SIM_NUMBER_2_STD).equals_division(INT_NUMBER, NUMBER2)
	assert SimNumberTester(INT_NUMBER / SIM_NUMBER_2_NONE).equals_division(INT_NUMBER, NUMBER2)


def test_eq_operation():
	assert SIM_NUMBER_1_STD != SIM_NUMBER_1_NONE
	assert SIM_NUMBER_1_STD != SIM_NUMBER_2_STD
	assert SIM_NUMBER_1_STD != SIM_NUMBER_2_NONE
	assert SIM_NUMBER_1_NONE != SIM_NUMBER_2_STD
	assert SIM_NUMBER_1_NONE != SIM_NUMBER_2_NONE
	assert SIM_NUMBER_2_STD != SIM_NUMBER_2_NONE

	assert SIM_NUMBER_1_STD == SIM_NUMBER_1_STD
	assert SIM_NUMBER_1_NONE == SIM_NUMBER_1_NONE
	assert SIM_NUMBER_2_STD == SIM_NUMBER_2_STD
	assert SIM_NUMBER_2_NONE == SIM_NUMBER_2_NONE

	assert SIM_NUMBER_1_STD != NUMBER1
	assert SIM_NUMBER_1_NONE == NUMBER1
	assert SIM_NUMBER_2_STD != NUMBER2
	assert SIM_NUMBER_2_NONE == NUMBER2

	assert SIM_NUMBER_1_STD != NUMBER2
	assert SIM_NUMBER_1_NONE != NUMBER2
	assert SIM_NUMBER_2_STD != NUMBER1
	assert SIM_NUMBER_2_NONE != NUMBER1


def test_bool_operation():
	assert SIM_NUMBER_1_STD
	assert SIM_NUMBER_1_NONE
	assert SIM_NUMBER_2_STD
	assert SIM_NUMBER_2_NONE

	assert not SimNumber(0)
	assert SimNumber(0.1)
	assert SimNumber(2)
	assert SimNumber(-2)

	assert not SimNumber(0, Prefix.NONE)
	assert SimNumber(0.1, Prefix.NONE)
	assert SimNumber(2, Prefix.NONE)
	assert SimNumber(-2, Prefix.NONE)

	assert not SimNumber(0, Prefix.STANDARD)
	assert SimNumber(0.1, Prefix.STANDARD)
	assert SimNumber(2, Prefix.STANDARD)
	assert SimNumber(-2, Prefix.STANDARD)

	assert not SimNumber(0, Prefix.QUETTA)
	assert SimNumber(0.1, Prefix.QUETTA)
	assert SimNumber(2, Prefix.QUETTA)
	assert SimNumber(-2, Prefix.QUETTA)

	assert not SimNumber(0, Prefix.QUECTO)
	assert SimNumber(0.1, Prefix.QUECTO)
	assert SimNumber(2, Prefix.QUECTO)
	assert SimNumber(-2, Prefix.QUECTO)


def test_str_operation():
	assert str(SIM_NUMBER_1_STD) == "54"
	assert str(SIM_NUMBER_1_NONE) == "54"
	assert str(SIM_NUMBER_2_STD) == "15"
	assert str(SIM_NUMBER_2_NONE) == "15"

	assert str(SimNumber(NUMBER1, Prefix.QUECTO)) == "54q"
	assert str(SimNumber(NUMBER2, Prefix.QUECTO)) == "15q"

	assert str(SimNumber(NUMBER1, Prefix.DECA)) == "54da"
	assert str(SimNumber(NUMBER2, Prefix.DECA)) == "15da"

	assert str(SimNumber(NUMBER1, Prefix.NONE)) == "54"
	assert str(SimNumber(NUMBER2, Prefix.NONE)) == "15"

	assert str(SimNumber(NUMBER1, Prefix.STANDARD)) == "54"
	assert str(SimNumber(NUMBER2, Prefix.STANDARD)) == "15"


def test_basic_operations_to_100():
	for i in range(1, 100):
		sim_number_1_std = SimNumber(i, Prefix.STANDARD)
		sim_number_1_none = SimNumber(i, Prefix.NONE)

		# Test __str__
		assert str(sim_number_1_std) == str(i)
		assert str(sim_number_1_none) == str(i)

		# Test __eq__
		assert sim_number_1_std != i
		assert sim_number_1_none == i

		assert i != sim_number_1_std
		assert i == sim_number_1_none

		assert sim_number_1_std == sim_number_1_std
		assert sim_number_1_std != sim_number_1_none

		assert sim_number_1_none == sim_number_1_none
		assert sim_number_1_none != sim_number_1_std

		# Test __bool__
		if i == 0:
			assert not sim_number_1_std
			assert not sim_number_1_none
		else:
			assert sim_number_1_std
			assert sim_number_1_none

		for j in range(100):
			sim_number_2_std = SimNumber(j, Prefix.STANDARD)
			sim_number_2_none = SimNumber(j, Prefix.NONE)

			numbers_for_calcs = [sim_number_1_std, sim_number_1_none, sim_number_2_std, sim_number_2_none]
			int_numbers_used = [i, i, j, j]

			for k in range(len(numbers_for_calcs)):
				for l in range(len(numbers_for_calcs)):
					# Test __add__
					assert (numbers_for_calcs[k] + numbers_for_calcs[l]).get_unsafe_number() == int_numbers_used[k] + int_numbers_used[l]
					# Test __sub__
					assert (numbers_for_calcs[k] - numbers_for_calcs[l]).get_unsafe_number() == int_numbers_used[k] - int_numbers_used[l]
					# Test __mult__
					assert (numbers_for_calcs[k] * numbers_for_calcs[l]).get_unsafe_number() == int_numbers_used[k] * int_numbers_used[l]
					if numbers_for_calcs[l].get_unsafe_number() != 0:
						# Test __floordiv__
						assert (numbers_for_calcs[k] // numbers_for_calcs[l]).get_unsafe_number() == int_numbers_used[k] // int_numbers_used[l]
						# Test __mod__
						assert (numbers_for_calcs[k] % numbers_for_calcs[l]).get_unsafe_number() == int_numbers_used[k] % int_numbers_used[l]
						# Test __divmod__
						assert divmod(numbers_for_calcs[k], numbers_for_calcs[l])[0].get_unsafe_number() == int_numbers_used[k] // int_numbers_used[l]
						assert divmod(numbers_for_calcs[k], numbers_for_calcs[l])[1].get_unsafe_number() == int_numbers_used[k] % int_numbers_used[l]
						# Test __truediv__
						print("%d / %d = %f" % (int_numbers_used[k], int_numbers_used[l], int_numbers_used[k] / int_numbers_used[l]))
						print("%f" % (numbers_for_calcs[k] / numbers_for_calcs[l]).get_unsafe_number())
						assert abs((numbers_for_calcs[k] / numbers_for_calcs[l]).get_unsafe_number() - int_numbers_used[k] / int_numbers_used[l]) <= MIN_ERROR
						# if numbers_for_calcs[k].get_prefix() == Prefix.NONE and numbers_for_calcs[l].get_prefix() == Prefix.NONE:
						#	assert numbers_for_calcs[k] / numbers_for_calcs[l] == int_numbers_used[k] / int_numbers_used[l]




