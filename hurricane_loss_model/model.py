import numpy as np
from numpy.random import poisson, lognormal
from typing import List
import logging


class LocationProfile():
    """
    Wrapper class that contains information about the location.
    """

    def __init__(self, landfall_rate: float, loss_prob_mean: float,
                 loss_prob_stddev: float) -> None:
        """
        Parameters
        ----------
        landfall_rate: float
            The anuual rate of landfalling hurricanes in the location.
        loss_prob_mean: float
            The mean of the probability distribution describing economic loss
            at the location.
        loss_prob_stddev: float
            The standard deviation of the probability distribution describing
            economic loss at the location.
        """
        self.landfall_rate = landfall_rate
        self.loss_prob_mean = loss_prob_mean
        self.loss_prob_stddev = loss_prob_stddev


class GenerateLossCalculation():
    """
    Prepare and run total loss calculation for a single location for many
    sample years.

    Methods
    -------
    run()
        Runs the calculation.
    """

    def __init__(self, location_profile: LocationProfile,
                 n_samples=1000) -> None:
        """
        Parameters
        ----------
        location_profile: LocationProfile
            The location profile for the location to run the simulation on.
        n_samples: int
            The number of sample years to run the simulation for.
        """
        self.loc = location_profile
        self.n = n_samples

    def run(self) -> float:
        """
        Run the total loss simulation for the given number of years.
        """
        num_events = poisson(self.loc.landfall_rate, self.n)
        loss_per_event = lognormal(mean=self.loc.loss_prob_mean,
                                   sigma=self.loc.loss_prob_stddev,
                                   size=sum(num_events))

        return np.sum(loss_per_event)


def run_loss_calculations(locations: List[LocationProfile],
                          n_samples: int) -> float:
    """
    Calculate the average annual loss in $Billions for a list of locations.

    Parameters
    ----------
    locations: [LocationProfile]
        List of location profiles describing all the locations to run the
        simulation on.
    n_samples: int
        The number of sample years to average over.
    """
    total_losses = 0
    for i, location in enumerate(locations):
        lossCalculation = GenerateLossCalculation(location, n_samples)
        logging.info(f'Calculated loss for location {i}/{len(locations)}')
        total_losses += lossCalculation.run()

    return total_losses / n_samples # mean loss
