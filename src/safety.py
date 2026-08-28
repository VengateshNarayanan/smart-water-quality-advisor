from typing import Dict


# --------------------------------------------------
# TURBIDITY SAFETY THRESHOLDS
# --------------------------------------------------
# These thresholds are application-level advisory
# categories, not a claim of legal drinking-water limits.

TURBIDITY_THRESHOLDS = {
    "low": 5.0,
    "moderate": 10.0,
    "high": 50.0
}


def assess_turbidity(turbidity: float) -> Dict:
    """
    Classify turbidity and generate a basic advisory.

    Categories:
        <= 5 NTU      -> Low
        <= 10 NTU     -> Moderate
        <= 50 NTU     -> High
        > 50 NTU      -> Critical
    """

    turbidity = float(turbidity)

    if turbidity <= TURBIDITY_THRESHOLDS["low"]:

        level = "Low"

        advisory = (
            "Turbidity is currently in the low range. "
            "Continue routine monitoring."
        )

    elif turbidity <= TURBIDITY_THRESHOLDS["moderate"]:

        level = "Moderate"

        advisory = (
            "Turbidity is elevated. "
            "Increase monitoring and investigate "
            "possible changes in water conditions."
        )

    elif turbidity <= TURBIDITY_THRESHOLDS["high"]:

        level = "High"

        advisory = (
            "Turbidity is high. "
            "Closer monitoring is recommended, "
            "and the source of the increase should be investigated."
        )

    else:

        level = "Critical"

        advisory = (
            "Turbidity is critically elevated. "
            "Immediate investigation and appropriate "
            "water-safety precautions are recommended."
        )

    return {
        "parameter": "Turbidity",
        "value": turbidity,
        "unit": "NTU",
        "level": level,
        "advisory": advisory
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_values = [
        2,
        7,
        25,
        75
    ]

    print("=" * 60)
    print("TURBIDITY SAFETY ENGINE TEST")
    print("=" * 60)

    for value in test_values:

        result = assess_turbidity(value)

        print(
            f"\n{value} NTU"
            f" → {result['level']}"
        )

        print(
            result["advisory"]
        )