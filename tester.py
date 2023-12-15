# ------------------------
# Tester class for the physics simulation
# Tests the GUI and the simulation logic
# ------------------------

import logging
import pytest

from simulator.test import test_sim_number


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

retcode = pytest.main()

