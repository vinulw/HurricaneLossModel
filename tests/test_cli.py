from hurricane_loss_model.cli import create_parser, validate_arguments
import pytest


def test_parser_valid():
    validArgs = [str(i) for i in range(1, 7)]

    # Check basic usage
    parser = create_parser()
    parsed = parser.parse_args(validArgs)

    assert parsed.florida_landfall_rate == 1.0
    assert parsed.gulf_landfall_rate == 4.0

    # Check with options
    validArgs = ['-n', '10'] + validArgs

    parsed = parser.parse_args(validArgs)

    assert isinstance(parsed.num_monte_carlo_samples, int)
    assert parsed.num_monte_carlo_samples == 10
    assert parsed.florida_landfall_rate == 1.0
    assert parsed.gulf_landfall_rate == 4.0


def test_parser_invalid(capsys):
    invalid_arguments = [
        (
            [],  # no arguments passed
            "arguments are required"
        ),
        (
            ['1', '1', '1', '1', '1', 'a'],  # invalid character
            "invalid float value"
        ),
        (
            ['-n', 'a', '1', '1', '1', '1', '1'],  # invalid optional character
            "invalid int value"
        )
    ]

    for invalid in invalid_arguments:
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(invalid[0])
        assert invalid[1] in capsys.readouterr().err


def test_validate_arguments():
    validArgs = ['1', '1', '1', '1', '1', '1']

    parser = create_parser()
    args = parser.parse_args(validArgs)

    assert validate_arguments(args) is None

    # Negative landfall rate
    invalidArgs = validArgs
    invalidArgs[0] = '-1'

    args = parser.parse_args(invalidArgs)

    with pytest.raises(ValueError) as excinfo:
        args = parser.parse_args(invalidArgs)
        validate_arguments(args)
    assert excinfo.type is ValueError, 'Landfall rate validation fail'

    # Negative standard deviation
    invalidArgs = validArgs
    invalidArgs[2] = '-1'

    with pytest.raises(ValueError) as excinfo:
        args = parser.parse_args(invalidArgs)
        validate_arguments(args)
    assert excinfo.type is ValueError, 'Std validation fail'

    # Negative standard deviation
    invalidArgs = ['-n', '-1'] + validArgs

    with pytest.raises(ValueError) as excinfo:
        args = parser.parse_args(invalidArgs)
        validate_arguments(args)
    assert excinfo.type is ValueError, 'Num samples validation fail'
