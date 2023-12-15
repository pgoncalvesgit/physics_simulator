# ------------------------
# Main class for the physics simulation
# Joins the GUI with the simulation logic
# ------------------------

from gui.api import endpoints as api
from simulator.si_units.si_converter import convert_with_precision, Prefix
from simulator.config.constants import *

print("result: " + str(convert_with_precision(AVOGADRO_NUMBER, Prefix.NONE, Prefix.YOTTA)))

print(api)
api.create_screen(1000, 700)
api.run()

api.quit_screen(0)

