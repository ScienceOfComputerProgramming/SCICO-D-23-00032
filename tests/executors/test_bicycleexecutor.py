from unittest.mock import MagicMock
import pytest
import numpy as np
from shapely import geometry

from frenetic.core.objective import MaxObjective
from frenetic.executors.abstract_executor import Outcome
from frenetic.executors.bicycle.bicycleexecutor import BicycleExecutor
from frenetic.representations import cartesian_generator
from frenetic.utils import geometry_utils

test = [(0,0), (0,50), (50,50), (75,100), (100, 100)]

@pytest.fixture
def centerline():
    original_line = geometry.LineString(np.array(test))
    return geometry_utils.cubic_spline(original_line)


@pytest.fixture
def bic_executor():
    return BicycleExecutor(representation=cartesian_generator.CatmullRomGenerator(control_nodes=30, variation=5),
                           objective=MaxObjective(
                               "distance_from_center",
                               per_simulation_aggregator="max"
                           ),
                           normalizer=None)

class TestBicycleExecutor(object):

    def test_dummy(self, bic_executor, centerline):
        result_dict = bic_executor._execute(test=list(centerline.coords))
        pass


