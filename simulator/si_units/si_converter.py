from .si_prefixes import prefix_to_base_10, PREFIX_TO_EXP, PREFIX_TO_STR
from ..config.config import HIGH_PRECISION_FORCE


class ImpossibleConversion(Exception):
    pass


def convert_with_precision(num, from_prefix, to_prefix):
    from_prefix_base_10_exponent = PREFIX_TO_EXP[from_prefix]
    to_prefix_base_10_exponent = PREFIX_TO_EXP[to_prefix]

    result: int
    if from_prefix_base_10_exponent == to_prefix_base_10_exponent:
        result = num

    elif from_prefix_base_10_exponent > to_prefix_base_10_exponent:
        result = num * pow(10, from_prefix_base_10_exponent - to_prefix_base_10_exponent)

    else:
        diff_exp = from_prefix_base_10_exponent - to_prefix_base_10_exponent
        reduced_num = num
        while diff_exp != 0 and reduced_num // 10 * 10 == reduced_num:
            reduced_num = reduced_num // 10
            diff_exp += 1
        result = reduced_num
        if diff_exp != 0:
            result = float(result)
        while diff_exp < 0:
            result = result / 10
            diff_exp += 1
    if result != int(result):
        print("Num: %s can't be converted from %s to %s" % (str(num), PREFIX_TO_STR[from_prefix], PREFIX_TO_STR[to_prefix]))
        if HIGH_PRECISION_FORCE:
            raise ImpossibleConversion
        else:
            return result
    return int(result)


def convert(num, from_prefix, to_prefix):
    from_prefix_base_10_exponent = PREFIX_TO_EXP[from_prefix]
    to_prefix_base_10_exponent = PREFIX_TO_EXP[to_prefix]

    if from_prefix_base_10_exponent == to_prefix_base_10_exponent:
        return num

    if from_prefix_base_10_exponent > to_prefix_base_10_exponent:
        return num * pow(10, from_prefix_base_10_exponent - to_prefix_base_10_exponent)

    else:
        return num * prefix_to_base_10(from_prefix) / prefix_to_base_10(to_prefix)
