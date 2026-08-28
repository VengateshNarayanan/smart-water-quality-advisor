
// ============================================================
// SMART WATER QUALITY ADVISORY ASSISTANT
// FRONTEND JAVASCRIPT
// ============================================================


// ============================================================
// LOAD ADVISORY
// ============================================================

async function loadAdvisory() {

    const systemStatus =
        document.getElementById("systemStatus");

    const riskBadge =
        document.getElementById("riskBadge");

    const currentTurbidity =
        document.getElementById("currentTurbidity");

    const predictedTurbidity =
        document.getElementById("predictedTurbidity");

    const timestamp =
        document.getElementById("timestamp");

    const safetyAdvisory =
        document.getElementById("safetyAdvisory");

    const aiRecommendation =
        document.getElementById("aiRecommendation");


    if (systemStatus) {
        systemStatus.textContent =
            "Generating analysis...";
    }


    try {

        const response =
            await fetch("/api/advisory", {
                method: "GET",
                cache: "no-store"
            });


        const result =
            await response.json();


        console.log(
            "[ADVISORY RESPONSE]",
            result
        );


        if (!result.success) {

            throw new Error(
                result.error ||
                "Unable to generate advisory."
            );
        }


        const assessment =
            result.data.assessment;

        const recommendation =
            result.data.recommendation;


        if (currentTurbidity) {

            currentTurbidity.textContent =
                Number(
                    assessment.current_turbidity
                ).toFixed(2);
        }


        if (predictedTurbidity) {

            predictedTurbidity.textContent =
                Number(
                    assessment.predicted_turbidity
                ).toFixed(2);
        }


        if (timestamp) {

            timestamp.textContent =
                assessment.timestamp;
        }


        if (riskBadge) {

            riskBadge.textContent =
                assessment.risk_level;
        }


        if (safetyAdvisory) {

            safetyAdvisory.textContent =
                assessment.safety_advisory;
        }


        if (aiRecommendation) {

            aiRecommendation.textContent =
                recommendation;
        }


        if (systemStatus) {

            systemStatus.textContent =
                "Analysis complete";
        }

    }

    catch (error) {

        console.error(
            "[ADVISORY ERROR]",
            error
        );


        if (systemStatus) {

            systemStatus.textContent =
                "Analysis failed";
        }


        if (riskBadge) {

            riskBadge.textContent =
                "ERROR";
        }


        if (aiRecommendation) {

            aiRecommendation.textContent =
                "Unable to generate the AI advisory.";
        }
    }
}



// ============================================================
// ADD CHAT MESSAGE
// ============================================================

function addChatMessage(
    sender,
    message,
    type
) {

    const chatMessages =
        document.getElementById(
            "chatMessages"
        );


    if (!chatMessages) {

        console.error(
            "chatMessages element not found."
        );

        return;
    }


    const messageDiv =
        document.createElement("div");


    messageDiv.className =
        "chat-message " + type;


    const strong =
        document.createElement("strong");


    strong.textContent =
        sender;


    const paragraph =
        document.createElement("p");


    paragraph.textContent =
        message;


    messageDiv.appendChild(
        strong
    );


    messageDiv.appendChild(
        paragraph
    );


    chatMessages.appendChild(
        messageDiv
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}



// ============================================================
// SEND CHAT MESSAGE
// ============================================================

async function sendChatMessage() {

    const input =
        document.getElementById(
            "chatInput"
        );


    const sendButton =
        document.getElementById(
            "sendButton"
        );


    if (!input || !sendButton) {

        console.error(
            "Chat input or send button not found."
        );

        return;
    }


    const message =
        input.value.trim();


    if (!message) {

        return;
    }


    // --------------------------------------------------------
    // Display user's message
    // --------------------------------------------------------

    addChatMessage(
        "You",
        message,
        "user"
    );


    // --------------------------------------------------------
    // Disable button
    // --------------------------------------------------------

    input.disabled = true;

    sendButton.disabled = true;

    sendButton.textContent =
        "Thinking...";


    try {

        console.log(
            "[CHAT] Sending:",
            message
        );


        // ----------------------------------------------------
        // Send request to Flask
        // ----------------------------------------------------

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    }),

                    cache: "no-store"
                }
            );


        console.log(
            "[CHAT] HTTP status:",
            response.status
        );


        // ----------------------------------------------------
        // Read JSON response
        // ----------------------------------------------------

        const result =
            await response.json();


        console.log(
            "[CHAT] Server response:",
            result
        );


        // ----------------------------------------------------
        // Check response
        // ----------------------------------------------------

        if (!result.success) {

            throw new Error(
                result.message ||
                result.error ||
                "Unable to process question."
            );
        }


        // ----------------------------------------------------
        // Display AI response
        // ----------------------------------------------------

        addChatMessage(
            "Water Advisor",
            result.message,
            "assistant"
        );


    }

    catch (error) {

        console.error(
            "[CHAT ERROR]",
            error
        );


        addChatMessage(
            "Water Advisor",
            "I was unable to process your question. " +
            "Please try again.",
            "assistant"
        );

    }

    finally {

        input.disabled = false;

        sendButton.disabled = false;

        sendButton.textContent =
            "Send";

        input.focus();
    }
}



// ============================================================
// INITIALIZE APPLICATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "Smart Water Quality Advisory Assistant loaded."
        );


        // ----------------------------------------------------
        // Refresh button
        // ----------------------------------------------------

        const refreshButton =
            document.getElementById(
                "refreshButton"
            );


        if (refreshButton) {

            refreshButton.addEventListener(
                "click",
                loadAdvisory
            );
        }


        // ----------------------------------------------------
        // Chat send button
        // ----------------------------------------------------

        const sendButton =
            document.getElementById(
                "sendButton"
            );


        if (sendButton) {

            sendButton.addEventListener(
                "click",
                sendChatMessage
            );
        }


        // ----------------------------------------------------
        // Chat input
        // ----------------------------------------------------

        const chatInput =
            document.getElementById(
                "chatInput"
            );


        if (chatInput) {

            chatInput.addEventListener(
                "keydown",
                function (event) {

                    if (event.key === "Enter") {

                        event.preventDefault();

                        sendChatMessage();
                    }
                }
            );
        }


        // ----------------------------------------------------
        // Initial advisory
        // ----------------------------------------------------

        loadAdvisory();

    }
);

