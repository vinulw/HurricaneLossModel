import numpy as np
from numpy.random import poisson, lognormal


class LocationProfile():
    """
    Wrapper class that contains information about the location.
    """

    def __init__(self, landfall_rate, loss_prob_mean, loss_prob_stddev):
        self.landfall_rate = landfall_rate
        self.loss_prob_mean = loss_prob_mean
        self.loss_prob_stddev = loss_prob_stddev


class GenerateLossCalculation():
    """
    Prepare and run total loss calculation for a single location.
    """

    def __init__(self, location_profile, n_samples=1000):
        self.loc = location_profile
        self.n = n_samples

    def run(self):
        num_events = poisson(self.loc.landfall_rate, self.n)
        loss_per_event = lognormal(mean=self.loc.loss_prob_mean,
                                   sigma=self.loc.loss_prob_stddev,
                                   size=sum(num_events))

        return np.sum(loss_per_event)


def runLossCalculations(locations, n_samples):
    """
    Calculate the average annual loss in $Billions for a list of locations.
    """
    total_losses = 0
    for location in locations:
        lossCalculation = GenerateLossCalculation(location, n_samples)
        total_losses += lossCalculation.run()

    return total_losses / n_samples