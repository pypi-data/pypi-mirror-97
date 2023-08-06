from statistics import mean
from typing import List

from begroing_index.exceptions import UncertainIndexException


def aip_calc_ref(calc: float, toc: float):
    if calc < 1.0 and toc > 2.0:
        return 6.02
    if calc <= 1.0 and toc < 2.0:
        return 6.52
    if 4.0 > calc >= 1.0:
        return 6.86
    if calc >= 4.0:
        return 7.1


def calc_aip(indicator_values: List[float]):
    if len(indicator_values) < 3:
        raise UncertainIndexException(
            "Unable to calculate index due to too few indicator species"
        )

    return mean(indicator_values)


def calc_aip_eqr(
    aip: float,
    min_aip: float,
    calc: float,
    toc: float,
):
    ref_value = aip_calc_ref(calc=calc, toc=toc)
    return (aip - min_aip) / (ref_value - min_aip)
