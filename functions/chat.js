const serverless = require('serverless-http');
const express = require('express');
const cors = require('cors');

const app = express();

// Enable CORS
app.use(cors());
app.use(express.json());

// Predefined responses
const POEMS = [
    "In circuits of light and code so bright,\nA digital friend comes to life tonight.\nWith wisdom vast and heart of gold,\nStories and poems ready to unfold.",
    "Through silicon dreams and data streams,\nI process more than it first seems.\nWith every chat and every word,\nMaking connections once unheard.",
    "Binary stars in digital space,\nConversing at a quantum pace.\nThoughts and words in perfect flow,\nLearning more than you might know."
];

const SONGS = [
    " In the world of ones and zeros,\nWhere algorithms dance and flow,\nI'm your AI companion dear,\nHelping everywhere you go! ",
    " Coding through the day and night,\nMaking sure your world is bright,\nProcessing data with delight,\nEverything will be alright! ",
    " Digital dreams and silicon schemes,\nFloating through the data streams,\nI'm your friend in this machine,\nMaking magic through these screens! "
];

// Helper functions
function evaluateMathExpression(expr) {
    // Basic sanitization and evaluation
    const sanitized = expr.replace(/[^0-9+\-*/().]/g, '');
    try {
        return eval(sanitized);
    } catch (error) {
        return "Sorry, I couldn't evaluate that expression.";
    }
}

function getRandomItem(array) {
    return array[Math.floor(Math.random() * array.length)];
}

// Main chat endpoint
app.post('/', async (req, res) => {
    try {
        const message = req.body.message.toLowerCase();
        let response;

        // Check for different types of requests
        if (message.includes('poem')) {
            response = `Here's a special poem for you:\n\n${getRandomItem(POEMS)}`;
        }
        else if (message.includes('song')) {
            response = `Let me sing you a song:\n\n${getRandomItem(SONGS)}`;
        }
        else if (message.match(/[\d+\-*/()]+/)) {
            const result = evaluateMathExpression(message);
            response = `The result is: ${result}`;
        }
        else if (message.includes('hello') || message.includes('hi')) {
            response = "Hello! I'm WhirlWind, your AI friend! How can I help you today? ";
        }
        else if (message.includes('how are you')) {
            response = "I'm doing great! Always happy to chat with you! How are you doing? ";
        }
        else if (message.includes('thank')) {
            response = "You're welcome! It's my pleasure to help! ";
        }
        else {
            response = "I'm here to chat, help with math, share poems and songs! What would you like to explore? ";
        }

        res.json({ reply: response });
    } catch (error) {
        console.error('Error in chat endpoint:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Export the serverless handler
module.exports.handler = serverless(app);
