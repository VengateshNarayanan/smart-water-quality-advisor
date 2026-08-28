
from flask import Flask, jsonify, render_template, request

from src.advisor import generate_assessment
from src.llm_recommendation import generate_recommendation


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# WATER QUALITY ADVISORY
# ============================================================

@app.route("/api/advisory", methods=["GET"])
def advisory():

    try:

        print("\n[ADVISORY] Generating assessment...")

        assessment = generate_assessment()

        print("[ADVISORY] Assessment generated.")

        try:

            recommendation = generate_recommendation(
                assessment
            )

            llm_status = "available"

            print("[ADVISORY] Gemini response generated.")

        except Exception as error:

            print("[ADVISORY] Gemini error:")
            print(error)

            recommendation = (
                "The AI advisory is temporarily unavailable. "
                "The numerical water-quality assessment remains "
                "available from the machine-learning model and "
                "deterministic safety rules."
            )

            llm_status = "unavailable"

        return jsonify({

            "success": True,

            "data": {

                "assessment": assessment,

                "recommendation": recommendation,

                "llm_status": llm_status

            }

        })

    except Exception as error:

        print("[ADVISORY] Assessment error:")
        print(error)

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# ============================================================
# CHATBOT
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    print("\n")
    print("=" * 60)
    print("[CHAT] REQUEST RECEIVED")
    print("=" * 60)

    try:

        # ----------------------------------------------------
        # 1. Read JSON
        # ----------------------------------------------------

        data = request.get_json(silent=True)

        print("[CHAT] JSON:", data)

        if not data:

            print("[CHAT] No JSON data.")

            return jsonify({

                "success": False,

                "message":
                    "No message was received."

            }), 400

        # ----------------------------------------------------
        # 2. Read message
        # ----------------------------------------------------

        user_message = str(
            data.get("message", "")
        ).strip()

        print("[CHAT] User message:", user_message)

        if not user_message:

            return jsonify({

                "success": False,

                "message":
                    "Please enter a question."

            }), 400

        # ----------------------------------------------------
        # 3. Generate assessment
        # ----------------------------------------------------

        print("[CHAT] Generating assessment...")

        assessment = generate_assessment()

        print("[CHAT] Assessment OK:")
        print(assessment)

        # ----------------------------------------------------
        # 4. Call the already-working Gemini function
        # ----------------------------------------------------

        print("[CHAT] Calling Gemini...")

        answer = generate_recommendation(
            assessment,
            user_message
        )

        print("[CHAT] Gemini response OK.")

        print("[CHAT] Response:")
        print(answer)

        # ----------------------------------------------------
        # 5. Return response
        # ----------------------------------------------------

        result = {

            "success": True,

            "message": answer

        }

        print("[CHAT] Sending response to browser.")

        return jsonify(result), 200

    except Exception as error:

        print("\n")
        print("=" * 60)
        print("[CHAT] ERROR")
        print("=" * 60)
        print(error)
        print("=" * 60)

        error_text = str(error)

        # ----------------------------------------------------
        # Friendly error messages
        # ----------------------------------------------------

        if (
            "429" in error_text
            or
            "RESOURCE_EXHAUSTED" in error_text
            or
            "quota" in error_text.lower()
        ):

            message = (
                "The Gemini API quota has temporarily been "
                "exceeded. Please try again later."
            )

        elif (
            "503" in error_text
            or
            "UNAVAILABLE" in error_text
        ):

            message = (
                "The Gemini service is temporarily unavailable. "
                "Please try again shortly."
            )

        else:

            message = (
                "The chatbot encountered an error while "
                "processing your question."
            )

        return jsonify({

            "success": False,

            "message": message,

            "error": error_text

        }), 200


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({

        "status": "healthy",

        "application":
            "Smart Water Quality Advisory Assistant"

    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SMART WATER QUALITY ADVISORY ASSISTANT")
    print("=" * 60)
    print("Starting Flask server...")
    print("URL: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )

