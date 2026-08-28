from pathlib import Path
import sys


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))


# --------------------------------------------------
# IMPORT PROJECT MODULES
# --------------------------------------------------

from predict import predict_latest
from safety import assess_turbidity
from llm_recommendation import generate_recommendation


# --------------------------------------------------
# GENERATE QUANTITATIVE ASSESSMENT
# --------------------------------------------------

def generate_assessment():

    prediction = predict_latest()

    safety = assess_turbidity(
        prediction["predicted_turbidity"]
    )

    return {
        "timestamp": str(
            prediction["timestamp"]
        ),

        "current_turbidity": round(
            prediction["current_turbidity"],
            4
        ),

        "predicted_turbidity": round(
            prediction["predicted_turbidity"],
            4
        ),

        "unit": "NTU",

        "risk_level": safety["level"],

        "safety_advisory": safety["advisory"]
    }


# --------------------------------------------------
# GENERATE COMPLETE ADVISORY
# --------------------------------------------------

def generate_complete_advisory():

    # Step 1:
    # Get verified numerical assessment
    assessment = generate_assessment()

    # Step 2:
    # Send ONLY verified information to the LLM
    recommendation = generate_recommendation(
        assessment
    )

    return {
        "assessment": assessment,
        "recommendation": recommendation
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("SMART WATER QUALITY ADVISORY ASSISTANT")
    print("STEP 11 - COMPLETE ADVISORY PIPELINE")
    print("=" * 60)

    result = generate_complete_advisory()

    assessment = result["assessment"]

    print("\n========== VERIFIED DATA ==========")

    print(
        f"Timestamp: "
        f"{assessment['timestamp']}"
    )

    print(
        f"Current Turbidity: "
        f"{assessment['current_turbidity']} NTU"
    )

    print(
        f"Predicted Turbidity: "
        f"{assessment['predicted_turbidity']} NTU"
    )

    print(
        f"Risk Level: "
        f"{assessment['risk_level']}"
    )

    print(
        "\n========== DETERMINISTIC ADVISORY =========="
    )

    print(
        assessment["safety_advisory"]
    )

    print(
        "\n========== LLM ADVISORY =========="
    )

    print(
        result["recommendation"]
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "COMPLETE ADVISORY PIPELINE SUCCESSFUL"
    )

    print(
        "=" * 60
    )