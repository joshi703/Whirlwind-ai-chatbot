document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.querySelector('.chat-container');
    const messageInput = document.querySelector('#message-input');
    const sendButton = document.querySelector('#send-button');

    function addMessage(message, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', isUser ? 'user-message' : 'bot-message');
        
        // Handle newlines in the message
        const formattedMessage = message.replace(/\n/g, '<br>');
        messageElement.innerHTML = formattedMessage;
        
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        try {
            // Disable input and button while sending
            messageInput.disabled = true;
            sendButton.disabled = true;

            // Add user message to chat
            addMessage(message, true);
            messageInput.value = '';

            // Send message to serverless function
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            addMessage(data.reply);
        } catch (error) {
            console.error('Error:', error);
            addMessage('Error: Failed to get response from server. Please try again.');
        } finally {
            // Re-enable input and button
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Initial greeting
    addMessage("Hello! I'm WhirlWind, your friendly AI assistant! I can help you with math, share poems and songs, or just chat! How can I help you today? 😊");
});
