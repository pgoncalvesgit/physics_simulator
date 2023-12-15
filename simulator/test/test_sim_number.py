from ..sim_number import SimNumber
from ..si_units.si_prefixes import  Prefix

NUMBER1 = 54
NUMBER2 = 15

SIM_NUMBER_1_STD = SimNumber(NUMBER1, Prefix.STANDARD)
SIM_NUMBER_2_STD = SimNumber(NUMBER2, Prefix.STANDARD)

SIM_NUMBER_1_NONE = SimNumber(NUMBER1, Prefix.NONE)
SIM_NUMBER_2_NONE = SimNumber(NUMBER2, Prefix.NONE)

INT_NUMBER = 3
FLOAT_NUMBER = 6.023


def test_add_operations():
	# check __add__
	assert (SIM_NUMBER_1_STD + SIM_NUMBER_2_STD).get_number() == NUMBER1 + NUMBER2
	assert (SIM_NUMBER_2_STD + SIM_NUMBER_1_STD).get_number() == NUMBER2 + NUMBER1
	assert (SIM_NUMBER_2_STD + SIM_NUMBER_1_STD).get_prefix() == Prefix.STANDARD

	assert (SIM_NUMBER_1_STD + SIM_NUMBER_2_NONE).get_number() == NUMBER1 + NUMBER2
	assert (SIM_NUMBER_1_STD + SIM_NUMBER_2_NONE).get_prefix() == Prefix.STANDARD

	assert (SIM_NUMBER_2_STD + SIM_NUMBER_1_NONE).get_number() == NUMBER2 + NUMBER1
	assert (SIM_NUMBER_2_STD + SIM_NUMBER_1_NONE).get_prefix() == Prefix.STANDARD

	assert (SIM_NUMBER_1_NONE + SIM_NUMBER_2_NONE).get_number() == NUMBER1 + NUMBER2
	assert (SIM_NUMBER_1_NONE + SIM_NUMBER_2_NONE).get_prefix() == Prefix.NONE
	assert (SIM_NUMBER_2_NONE + SIM_NUMBER_1_NONE).get_number() == NUMBER2 + NUMBER1
	assert (SIM_NUMBER_2_NONE + SIM_NUMBER_1_NONE).get_prefix() == Prefix.NONE

	assert (SIM_NUMBER_1_STD + INT_NUMBER).get_number() == NUMBER1 + INT_NUMBER
	assert (SIM_NUMBER_1_STD + INT_NUMBER).get_prefix() == Prefix.STANDARD
	assert (SIM_NUMBER_2_STD + INT_NUMBER).get_number() == NUMBER2 + INT_NUMBER
	assert (SIM_NUMBER_2_STD + INT_NUMBER).get_prefix() == Prefix.STANDARD

	# check __radd__
	assert (INT_NUMBER + SIM_NUMBER_1_STD).get_number() == INT_NUMBER + NUMBER1
	assert (INT_NUMBER + SIM_NUMBER_1_STD).get_prefix() == Prefix.STANDARD

	assert (INT_NUMBER + SIM_NUMBER_1_NONE).get_number() == INT_NUMBER + NUMBER1
	assert (INT_NUMBER + SIM_NUMBER_1_NONE).get_prefix() == Prefix.NONE

	assert (INT_NUMBER + SIM_NUMBER_2_STD).get_number() == INT_NUMBER + NUMBER2
	assert (INT_NUMBER + SIM_NUMBER_2_STD).get_prefix() == Prefix.STANDARD

	assert (INT_NUMBER + SIM_NUMBER_2_NONE).get_number() == INT_NUMBER + NUMBER2
	assert (INT_NUMBER + SIM_NUMBER_2_NONE).get_prefix() == Prefix.NONE


def test_sub_operations():
	# check __sub__
	assert (SIM_NUMBER_1_STD - SIM_NUMBER_2_STD).get_number() == NUMBER1 - NUMBER2
	assert (SIM_NUMBER_2_STD - SIM_NUMBER_1_STD).get_number() == NUMBER2 - NUMBER1
	assert (SIM_NUMBER_1_STD - SIM_NUMBER_2_NONE).get_number() == NUMBER1 - NUMBER2
	assert (SIM_NUMBER_2_STD - SIM_NUMBER_1_NONE).get_number() == NUMBER2 - NUMBER1
	assert (SIM_NUMBER_1_NONE - SIM_NUMBER_2_NONE).get_number() == NUMBER1 - NUMBER2
	assert (SIM_NUMBER_2_NONE - SIM_NUMBER_1_NONE).get_number() == NUMBER2 - NUMBER1
	assert (SIM_NUMBER_1_STD - INT_NUMBER).get_number() == NUMBER1 - INT_NUMBER
	assert (SIM_NUMBER_2_STD - INT_NUMBER).get_number() == NUMBER2 - INT_NUMBER

	# check __rsub__
	assert (INT_NUMBER - SIM_NUMBER_1_STD).get_number() == INT_NUMBER - NUMBER1
	assert (INT_NUMBER - SIM_NUMBER_2_STD).get_number() == INT_NUMBER - NUMBER2


def test_mul_operations():
	# check __mul__
	assert (SIM_NUMBER_1_STD * SIM_NUMBER_2_STD).get_number() == NUMBER1 * NUMBER2
	assert (SIM_NUMBER_2_STD * SIM_NUMBER_1_STD).get_number() == NUMBER2 * NUMBER1
	assert (SIM_NUMBER_1_STD * SIM_NUMBER_2_NONE).get_number() == NUMBER1 * NUMBER2
	assert (SIM_NUMBER_2_STD * SIM_NUMBER_1_NONE).get_number() == NUMBER2 * NUMBER1
	assert (SIM_NUMBER_1_NONE * SIM_NUMBER_2_NONE).get_number() == NUMBER1 * NUMBER2
	assert (SIM_NUMBER_2_NONE * SIM_NUMBER_1_NONE).get_number() == NUMBER2 * NUMBER1
	assert (SIM_NUMBER_1_STD * INT_NUMBER).get_number() == NUMBER1 * INT_NUMBER
	assert (SIM_NUMBER_2_STD * INT_NUMBER).get_number() == NUMBER2 * INT_NUMBER

	# check __rmul__
	assert (INT_NUMBER * SIM_NUMBER_1_STD).get_number() == INT_NUMBER * NUMBER1
	assert (INT_NUMBER * SIM_NUMBER_2_STD).get_number() == INT_NUMBER * NUMBER2


def test_floor_operations():
	# check __floor__
	assert (SIM_NUMBER_1_STD // SIM_NUMBER_2_STD).get_number() == NUMBER1 // NUMBER2
	assert (SIM_NUMBER_2_STD // SIM_NUMBER_1_STD).get_number() == NUMBER2 // NUMBER1
	assert (SIM_NUMBER_1_STD // SIM_NUMBER_2_NONE).get_number() == NUMBER1 // NUMBER2
	assert (SIM_NUMBER_2_STD // SIM_NUMBER_1_NONE).get_number() == NUMBER2 // NUMBER1
	assert (SIM_NUMBER_1_NONE // SIM_NUMBER_2_NONE).get_number() == NUMBER1 // NUMBER2
	assert (SIM_NUMBER_2_NONE // SIM_NUMBER_1_NONE).get_number() == NUMBER2 // NUMBER1
	assert (SIM_NUMBER_1_STD // INT_NUMBER).get_number() == NUMBER1 // INT_NUMBER
	assert (SIM_NUMBER_2_STD // INT_NUMBER).get_number() == NUMBER2 // INT_NUMBER

	# check __rfloor__
	assert (INT_NUMBER // SIM_NUMBER_1_STD).get_number() == INT_NUMBER // NUMBER1
	assert (INT_NUMBER // SIM_NUMBER_2_STD).get_number() == INT_NUMBER // NUMBER2


def test_mod_operations():
	# check __mod__
	assert (SIM_NUMBER_1_STD % SIM_NUMBER_2_STD).get_number() == NUMBER1 % NUMBER2
	assert (SIM_NUMBER_2_STD % SIM_NUMBER_1_STD).get_number() == NUMBER2 % NUMBER1
	assert (SIM_NUMBER_1_STD % SIM_NUMBER_2_NONE).get_number() == NUMBER1 % NUMBER2
	assert (SIM_NUMBER_2_STD % SIM_NUMBER_1_NONE).get_number() == NUMBER2 % NUMBER1
	assert (SIM_NUMBER_1_NONE % SIM_NUMBER_2_NONE).get_number() == NUMBER1 % NUMBER2
	assert (SIM_NUMBER_2_NONE % SIM_NUMBER_1_NONE).get_number() == NUMBER2 % NUMBER1
	assert (SIM_NUMBER_1_STD % INT_NUMBER).get_number() == NUMBER1 % INT_NUMBER
	assert (SIM_NUMBER_2_STD % INT_NUMBER).get_number() == NUMBER2 % INT_NUMBER

	# check __rmod__
	assert (INT_NUMBER % SIM_NUMBER_1_STD).get_number() == INT_NUMBER % NUMBER1
	assert (INT_NUMBER % SIM_NUMBER_2_STD).get_number() == INT_NUMBER % NUMBER2


# TODO
def test_divmod_operations():
	# check __divmod__
	assert (SIM_NUMBER_1_STD / SIM_NUMBER_2_STD).get_number() == NUMBER1 / NUMBER2
	assert (SIM_NUMBER_2_STD / SIM_NUMBER_1_STD).get_number() == NUMBER2 / NUMBER1
	assert (SIM_NUMBER_1_STD / SIM_NUMBER_2_NONE).get_number() == NUMBER1 / NUMBER2
	assert (SIM_NUMBER_2_STD / SIM_NUMBER_1_NONE).get_number() == NUMBER2 / NUMBER1
	assert (SIM_NUMBER_1_NONE / SIM_NUMBER_2_NONE).get_number() == NUMBER1 / NUMBER2
	assert (SIM_NUMBER_2_NONE / SIM_NUMBER_1_NONE).get_number() == NUMBER2 / NUMBER1
	assert (SIM_NUMBER_1_STD / INT_NUMBER).get_number() == NUMBER1 / INT_NUMBER
	assert (SIM_NUMBER_2_STD / INT_NUMBER).get_number() == NUMBER2 / INT_NUMBER

	# check __divmod__
	assert (INT_NUMBER / SIM_NUMBER_1_STD).get_number() == INT_NUMBER / NUMBER1
	assert (INT_NUMBER / SIM_NUMBER_2_STD).get_number() == INT_NUMBER / NUMBER2


def test_truediv_operations():
	# check __truediv__
	assert (SIM_NUMBER_1_STD / SIM_NUMBER_2_STD).get_number() == NUMBER1 / NUMBER2
	assert (SIM_NUMBER_2_STD / SIM_NUMBER_1_STD).get_number() == NUMBER2 / NUMBER1
	assert (SIM_NUMBER_1_STD / INT_NUMBER).get_number() == NUMBER1 / INT_NUMBER
	assert (SIM_NUMBER_2_STD / INT_NUMBER).get_number() == NUMBER2 / INT_NUMBER

	# check __truediv__
	assert (INT_NUMBER / SIM_NUMBER_1_STD).get_number() == INT_NUMBER / NUMBER1
	assert (INT_NUMBER / SIM_NUMBER_2_STD).get_number() == INT_NUMBER / NUMBER2


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
