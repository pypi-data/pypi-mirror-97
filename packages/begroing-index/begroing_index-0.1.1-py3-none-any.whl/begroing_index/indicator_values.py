import csv
import os
from statistics import mean
from typing import Dict

iv_files = {
    "PIT": "indicator_values_PIT.csv",
    "AIP": "indicator_values_AIP.csv",
}


def load_indicator_values(index_name: str) -> Dict[str, float]:
    indicator_values = {}
    with open(
        os.path.join(
            os.path.dirname(__file__), "../indicator_values", iv_files[index_name]
        )
    ) as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            if len(row.values()) != 2:
                raise Exception(f"Could not read csv line: {row}")
            iv = float(row["indicator_value"].strip())
            assert iv > 0
            latin_name = row["latin_name"].strip()
            assert len(latin_name) > 0
            indicator_values[latin_name] = iv
    return indicator_values


def calc_max_iv(indicator_values: Dict[str, float], min_species_count: int) -> float:
    sorted_iv = sorted(indicator_values.values(), reverse=True)
    top_values = sorted_iv[:min_species_count]
    return mean(top_values)


def calc_min_iv(indicator_values: Dict[str, float], min_species_count: int) -> float:
    sorted_iv = sorted(indicator_values.values())
    bottom_values = sorted_iv[:min_species_count]
    return mean(bottom_values)
