from statistics import mean
from typing import Final, List

from begroing_index.exceptions import UncertainIndexException


def pit_ref_value(calc: float):
    # taken from https://www.vannportalen.no/veiledning/klassifiserings/ table 5.1a
    # TODO: table 5.1a does not specify what to use for exact calc concentration 1

    return 4.85 if calc < 1 else 6.71


def calc_pit(indicator_values: List[float]):
    if len(indicator_values) < 2:
        raise UncertainIndexException(
            "Unable to calculate index due to too few indicator species"
        )

    # TODO: check if sampling has been done between june/october? perhaps do this somewhere else
    return mean(indicator_values)


def calc_pit_eqr(pit_value: float, max_pit: float, calc_consentration: float):
    ref_value = pit_ref_value(calc_consentration)
    return (pit_value - max_pit) / (ref_value - max_pit)
