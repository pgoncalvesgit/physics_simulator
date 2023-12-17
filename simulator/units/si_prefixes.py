from enum import Enum
from simulator.units import symbols as sy


class UnknownPrefix(Exception):
    pass


class Prefix(Enum):
    QUETTA = 1 * pow(10, 30)
    RONNA = 1 * pow(10, 27)
    YOTTA = 1 * pow(10, 24)
    ZETTA = 1 * pow(10, 21)
    EXA = 1 * pow(10, 18)
    PETA = 1 * pow(10, 15)
    TERA = 1 * pow(10, 12)
    GIGA = 1 * pow(10, 9)
    MEGA = 1 * pow(10, 6)
    KILO = 1 * pow(10, 3)
    HECTO = 1 * pow(10, 2)
    DECA = 1 * pow(10, 1)

    STANDARD = 1 * pow(10, 0)
    NONE = 2 * pow(10, 0)

    DECI = 1 * pow(10, -1)
    CENTI = 1 * pow(10, -2)
    MILLI = 1 * pow(10, -3)
    MICRO = 1 * pow(10, -6)
    NANO = 1 * pow(10, -9)
    PICO = 1 * pow(10, -12)
    FEMTO = 1 * pow(10, -15)
    ATTO = 1 * pow(10, -18)
    ZEPTO = 1 * pow(10, -21)
    YOCTO = 1 * pow(10, -24)
    RONTO = 1 * pow(10, -27)
    QUECTO = 1 * pow(10, -30)


PREFIX_TO_EXP = {
    Prefix.QUETTA: 30,
    Prefix.RONNA: 27,
    Prefix.YOTTA: 24,
    Prefix.ZETTA: 21,
    Prefix.EXA: 18,
    Prefix.PETA: 15,
    Prefix.TERA: 12,
    Prefix.GIGA: 9,
    Prefix.MEGA: 6,
    Prefix.KILO: 3,
    Prefix.HECTO: 2,
    Prefix.DECA: 1,
    Prefix.STANDARD: 0,
    Prefix.NONE: 0,
    Prefix.DECI: -1,
    Prefix.CENTI: -2,
    Prefix.MILLI: -3,
    Prefix.MICRO: -6,
    Prefix.NANO: -9,
    Prefix.PICO: -12,
    Prefix.FEMTO: -15,
    Prefix.ATTO: -18,
    Prefix.ZEPTO: -21,
    Prefix.YOCTO: -24,
    Prefix.RONTO: -27,
    Prefix.QUECTO: -30
}

__PREFIX_ITEMS_LIST = list(PREFIX_TO_EXP.items())

PREFIX_TO_STR = {
    Prefix.QUETTA: "Q",
    Prefix.RONNA: "R",
    Prefix.YOTTA: "Y",
    Prefix.ZETTA: "Z",
    Prefix.EXA: "E",
    Prefix.PETA: "P",
    Prefix.TERA: "T",
    Prefix.GIGA: "G",
    Prefix.MEGA: "M",
    Prefix.KILO: "k",
    Prefix.HECTO: "h",
    Prefix.DECA: "da",
    Prefix.STANDARD: "",
    Prefix.NONE: "",
    Prefix.DECI: "d",
    Prefix.CENTI: "c",
    Prefix.MILLI: "m",
    Prefix.MICRO: sy.MU_LOWER,
    Prefix.NANO: "n",
    Prefix.PICO: "p",
    Prefix.FEMTO: "f",
    Prefix.ATTO: "a",
    Prefix.ZEPTO: "z",
    Prefix.YOCTO: "y",
    Prefix.RONTO: "r",
    Prefix.QUECTO: "q"
}


LARGEST_PREFIX = Prefix.QUETTA
SMALLEST_PREFIX = Prefix.QUECTO
LARGEST_PREFIX_VALUE = PREFIX_TO_EXP[LARGEST_PREFIX]
SMALLEST_PREFIX_VALUE = PREFIX_TO_EXP[SMALLEST_PREFIX]


def return_smaller_prefix(prefix1: Prefix, prefix2: Prefix):
    if PREFIX_TO_EXP[prefix1] < PREFIX_TO_EXP[prefix2]:
        return prefix1
    return prefix2


def prefix_to_base_10(prefix):
    return 1 * pow(10, PREFIX_TO_EXP[prefix])


# TODO
def prefix_to_base_10_normalized(prefix):
    return 1 * pow(10, PREFIX_TO_EXP[prefix])


def floor_prefix(exp):
    mid_i = len(__PREFIX_ITEMS_LIST) // 2
    index = mid_i - exp // 3
    if __PREFIX_ITEMS_LIST[index][1] < exp:
        return __PREFIX_ITEMS_LIST[index][0]
    elif __PREFIX_ITEMS_LIST[index + 1][1] < exp:
        return __PREFIX_ITEMS_LIST[index][0]
    else:
        raise UnknownPrefix


