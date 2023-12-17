# ------------------------
# Tester class for the physics simulation
# Tests the GUI and the simulation logic
# ------------------------

import logging
import pytest


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

retcode = pytest.main()

