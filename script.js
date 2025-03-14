const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const microphoneBtn = document.querySelector(".fa-microphone"); // Microphone button
let userMessage = null; // Variable to store user's message
let sessionData = {}; // Object to store session data (like student type)
const inputInitHeight = chatInput.scrollHeight;

// Create a chat <li> element with passed message and className
const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing"
        ? `<p></p>`
        : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
};

// Delay function to prevent excessive API calls
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Generate response from Flask API
const generateResponse = async (chatElement) => {
    const messageElement = chatElement.querySelector("p");

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage, session_data: sessionData }), // Send session data
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/chat', requestOptions);
        if (response.status === 429) {
            messageElement.textContent = "Too many requests. Retrying...";
            await delay(2000); // Wait 2 seconds and retry
            return generateResponse(chatElement);
        } else if (!response.ok) {
            throw new Error("Failed to fetch response");
        }

        const data = await response.json();
        messageElement.textContent = data.reply.trim();
    } catch (error) {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
    } finally {
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }
};

// Handle chat input and API response
const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
};

// Adjust input field height as user types
chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

// Send message on Enter key press
chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

// Click event to send message
sendChatBtn.addEventListener("click", handleChat);

// Close chatbot
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));

// Toggle chatbot window visibility
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

// Implementing speech recognition for microphone icon
if ("SpeechRecognition" in window || "webkitSpeechRecognition" in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    let isListening = false; // Track listening state

    recognition.onstart = () => {
        microphoneBtn.classList.add("listening");
    };

    recognition.onend = () => {
        microphoneBtn.classList.remove("listening");
        isListening = false; // Reset listening state
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
        userMessage = transcript;
        handleChat();
    };

    recognition.onerror = (event) => {
        alert(`Speech recognition error: ${event.error}`);
        microphoneBtn.classList.remove("listening");
        isListening = false;
    };

    microphoneBtn.addEventListener("click", () => {
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
            isListening = true;
        }
    });
} else {
    microphoneBtn.style.display = "none"; // Hide the microphone button
    console.error("Speech Recognition is not supported in this browser.");
}
