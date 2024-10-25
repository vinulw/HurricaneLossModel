import argparse
from hurricane_loss_model.model import LocationProfile, run_loss_calculations

DEFAULT_SAMPLES = 1000


def create_parser():
    """
    Function create parser for command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog='gethurricaneloss',
        description="""
            Calculates the average annual hurricane loss in $Billions for
            a simple hurricane model.
            """
    )

    requiredArguments = [
        ('florida_landfall_rate',
         'The anuual rate of landfalling hurricanes in Florida.'),
        ('florida_mean',
         '''The LogNormal parameters that describe the economic loss of
         a landfalling hurricane in Florida.'''),
        ('florida_stddev', ''),
        ('gulf_landfall_rate',
         'The annual rate of landfalling hurricanes in the Gulf state.'),
        ('gulf_mean',
         '''The LogNormal parameters that describe the economic loss of
         a landfalling hurricane in the Gulf states.'''),
        ('gulf_stddev',
         '')
    ]

    for arg in requiredArguments:
        parser.add_argument(arg[0], help=arg[1], default=1000, type=float)

    # Add optional parameter
    parser.add_argument('-n', '--num_monte_carlo_samples', type=int,
                        help="""Number of samples (simulation years) to run
                        (default 1000).""")
    return parser


def validate_arguments(args):
    '''
    Validate parsed arguments for model specific use. Throws exception if
    validation fails.
    '''
    # Number of samples positive
    if (args.num_monte_carlo_samples is not None and
            args.num_monte_carlo_samples <= 0):
        raise ValueError("Number of samples has to be greater than 0")

    # Landfall rates positive
    if (args.florida_landfall_rate < 0 or args.gulf_landfall_rate < 0):
        raise ValueError("Landfall rate cannot be negative")

    # Standard deviation positive
    if (args.florida_stddev < 0 or args.gulf_stddev < 0):
        raise ValueError("Standard deviation cannot be negative")


def main():
    """
    Main function for CLI. It parses arguments and runs the model.
    """
    args = create_parser().parse_args()

    validate_arguments(args)

    num_samples = args.num_monte_carlo_samples

    if num_samples is None:
        num_samples = DEFAULT_SAMPLES

    floridaProfile = LocationProfile(args.florida_landfall_rate,
                                     args.florida_mean,
                                     args.florida_stddev)

    gulfProfile = LocationProfile(args.gulf_landfall_rate,
                                  args.gulf_mean,
                                  args.gulf_stddev)

    locations = [floridaProfile, gulfProfile]

    print(run_loss_calculations(locations, num_samples))
