import pytest
from hurricane_loss_model.model import GenerateLossCalculation, LocationProfile
from hurricane_loss_model.model import run_loss_calculations


# Constants

NUM_SAMPLES = 100


# Fixtures

@pytest.fixture
def loc_profile():
    return LocationProfile(1, 1, 1)


# Tests

def test_run_loss_calculation(loc_profile):
    loss_calculation = GenerateLossCalculation(loc_profile, NUM_SAMPLES)
    assert isinstance(loss_calculation.run(), float)


def test_zero_loss_calculation():
    '''
    Test zero rate of hurricanes produce no loss.
    '''
    loc_profile = LocationProfile(0, 1, 1)
    loss_calculation = GenerateLossCalculation(loc_profile, NUM_SAMPLES)
    assert loss_calculation.run() == 0.0, 'Zero hurricanes produce loss'


def test_run_multiple_locations(loc_profile):
    locations = [loc_profile, loc_profile]

    assert isinstance(run_loss_calculations(locations, NUM_SAMPLES), float)
