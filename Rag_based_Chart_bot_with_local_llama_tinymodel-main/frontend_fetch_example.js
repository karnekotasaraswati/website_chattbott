// Example Javascript fetch code to call your RAG Chatbot API
// You can use this in your frontend application (React, Vue, Plain JS, etc.)

async function sendMessageToChatbot(userMessage) {
    const API_URL = "http://localhost:8000/chat"; // Update if hosted elsewhere

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: userMessage
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Handle streaming response (assuming backend streams plain text)
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let botResponse = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, { stream: true });
            botResponse += chunk;
            
            // Update your UI here with the partial response
            console.log("Received chunk:", chunk);
            // updateChatUI(botResponse); 
        }
        
        console.log("Full response:", botResponse);
        return botResponse;

    } catch (error) {
        console.error("Error communicating with chatbot:", error);
        return "Sorry, I encountered an error.";
    }
}

// Usage example:
// sendMessageToChatbot("What skills are needed for a Data Scientist?");
