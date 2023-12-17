from simulator.units.si_prefixes import Prefix
from simulator.units.sim_number import SimNumber


class SimUnit(SimNumber):
	def __init__(self, number=0, prefix=Prefix.NONE):
		super().__init__(number, prefix)
		