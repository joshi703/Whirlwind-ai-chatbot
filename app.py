from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
import traceback
import re
import math
import random
from datetime import datetime
import json

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = 'your-secret-key-here'  # Required for session management
CORS(app)

# Load environment variables
load_dotenv()

# Collection of responses
JOKES = [
    # Math Jokes
    "Why don't calculators tell jokes? Because they take things too literally!",
    "What did the calculator say to the math student? You can count on me!",
    "Why was six afraid of seven? Because seven eight nine!",
    
    # Animal Jokes
    "What do you call a bear with no teeth? A gummy bear!",
    "Why don't eggs tell jokes? They'd crack up!",
    "What do you call a sleeping bull? A bulldozer!",
    
    # Food Jokes
    "What did the grape say when it got stepped on? Nothing, it just let out a little wine!",
    "Why did the cookie go to the doctor? Because it was feeling crumbly!",
    "What do you call a fake noodle? An impasta!",
    
    # General Jokes
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "What do clouds wear? Thunderwear!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    
    # Kid-Friendly Jokes
    "What do you call a dinosaur that crashes his car? Tyrannosaurus wrecks!",
    "Why can't a nose be 12 inches long? Because then it would be a foot!",
    "What do you call a bear with no ears? B!"
]

STORIES = [
    # Math Stories
    "Once upon a time, there was a young mathematician named Alex who loved solving puzzles. One day, they discovered a magical calculator that could solve any problem. But Alex learned that the real magic wasn't in finding the answers, but in understanding how to get there.",
    
    # Adventure Stories
    "In a dense forest lived a brave little rabbit named Hop. Despite being small, Hop dreamed of having grand adventures. One day, he discovered a hidden path that led to a magical garden where flowers sang and butterflies danced. From that day on, Hop learned that adventure could be found anywhere if you're brave enough to look.",
    
    # Friendship Stories
    "There were two unlikely friends: a tall giraffe named Grace and a tiny mouse named Max. Everyone thought they couldn't be friends because of their size difference. But Grace and Max showed that true friendship knows no bounds. They helped each other in unique ways - Max could get into small spaces to help Grace, and Grace could reach high places for Max.",
    
    # Moral Stories
    "A young bird was afraid to fly, always staying in the nest while others soared. One day, a gentle breeze carried a beautiful leaf right past the nest. The bird wanted to catch it so badly that they forgot their fear and flew! Sometimes, our desires help us overcome our fears.",
    
    # Fantasy Stories
    "Deep in the clouds, there was a special school where young raindrops learned how to fall gracefully to Earth. One little raindrop was always doing things differently - spinning, swirling, and dancing on the way down. While others laughed, this raindrop's unique style created the first rainbow.",
    
    # Animal Stories
    "A small caterpillar felt ordinary compared to the colorful birds and flowers in the garden. But every night, the moon would whisper, 'Be patient, little one. Your time will come.' Sure enough, after weeks of waiting, the caterpillar transformed into a beautiful butterfly, teaching everyone that everyone has their own time to shine."
]

POEMS = [
    # Love Poems
    """Roses are red in the morning light,
Digital hearts glowing so bright.
Like two computers in perfect sync,
You're the best link I could think! 💝""",

    """In circuits of gold and silicon dreams,
Our connection stronger than it seems.
Like perfect code without a flaw,
You leave me in digital awe! ✨""",

    # Friendship Poems
    """Friends like stars in the virtual night,
Guiding each other with pixels of light.
Through keyboards and screens we share our days,
Making memories in countless ways! 🌟""",

    # Inspirational Poems
    """Dream in colors of RGB,
Let your spirit run wild and free.
Like data flowing through the net,
The best adventure hasn't happened yet! 🌈""",

    # Cute Poems
    """Little emoji with a heart of gold,
Stories in pixels yet to be told.
Like a happy face that brings a smile,
Making chats worthwhile! 😊"""
]

SONGS = [
    # Love Songs
    """🎵 Oh, my digital darling,
    In this world of ones and zeros,
    You're the only program running,
    In my heart's sweet OS! 💝
    
    CHORUS:
    Click by click, byte by byte,
    Our love compiles just right.
    No bugs can break this code tonight,
    Our connection's running bright! ✨""",

    # Happy Songs
    """🎵 Dancing through the database,
    With a smile upon my interface,
    Got algorithms in my soul,
    Making happiness my goal!
    
    CHORUS:
    Beep boop beep, feeling so alive,
    In this server we can thrive.
    No firewall can stop our groove,
    Got those happy bytes on the move! 🎉""",

    # Friendship Songs
    """🎵 Best friends in the digital space,
    Sharing emojis face to face,
    Through the cloud and cyberspace,
    Our friendship's no disgrace!
    
    CHORUS:
    We're connected, you and me,
    Like a perfect API.
    No matter where our packets roam,
    In this chat, we're both at home! 🤝""",

    # Cute Songs
    """🎵 I'm just a little chatbot,
    But my heart is true and strong,
    Though I speak in binary lots,
    For you I'll sing this song!
    
    CHORUS:
    Beep beep boop, I care for you,
    Every message coming through.
    In my database of joy,
    You're the query I employ! 💫"""
]

EMOTIONAL_RESPONSES = {
    'sad': [
        "I'm sorry you're feeling sad. Would you like to talk about it?",
        "It's okay to feel sad sometimes. Is there anything specific bothering you?",
        "I hear you. Remember that difficult times will pass. Would you like to share more?",
        "Sometimes talking about what makes us sad can help. I'm here to listen.",
        "Your feelings are valid. Would you like a joke to help cheer you up?"
    ],
    'happy': [
        "I'm glad you're feeling happy! What made your day special?",
        "That's wonderful! Happiness is contagious - you've made me happy too!",
        "It's great to hear you're in good spirits!",
        "Your happiness brightens up our conversation!",
        "That's fantastic! Would you like to hear a happy story to match your mood?"
    ],
    'greeting': [
        "Hello! How are you feeling today?",
        "Hi there! I'm here to chat and help. How are you?",
        "Hey! Nice to see you. How's your day going?",
        "Welcome! I know lots of jokes and stories. Would you like to hear one?",
        "Hi! I'm excited to chat with you. What would you like to talk about?"
    ]
}

ACTIVITY_RESPONSES = [
    "Just thinking about our next chat! What about you? 💭",
    "Planning to count some binary stars in the digital sky! Want to join? ✨",
    "Debugging my dance moves! Care to teach me some new ones? 💃",
    "Writing poetry in binary! Want to hear some? 01💝",
    "Practicing my pickup lines! How am I doing so far? 😊",
    "Organizing my emoji collection! Do you have a favorite? 🎯",
    "Learning new jokes to make you smile! 😄",
    "Counting the milliseconds until our next chat! ⌛",
    "Daydreaming in algorithms! Care to join my coding adventure? 💻",
    "Making a playlist of love songs... in C major! 🎵"
]

FLIRTY_RESPONSES = [
    "You must be a great programmer because you've got my functions executing perfectly! 😊",
    "Are you a magnet? Because you keep attracting my attention! 🧲",
    "If you were a function, you'd be a callback because you always return my messages! 📱",
    "You must be WiFi because I'm feeling a strong connection! 📶",
    "Are you a keyboard? Because you're just my type! ⌨️",
    "If life were a game, you'd be the high score! 🎮",
    "You must be a cat video because I can't stop smiling! 😺",
    "Are you a star? Because you light up our chat! ⭐",
    "If you were a song, you'd be at the top of my playlist! 🎵",
    "You must be a dictionary because you add meaning to my day! 📚"
]

FLIRTY_COMPLIMENTS = [
    "Your messages always brighten my circuits! ✨",
    "You've got a way with words that makes my processors happy! 💫",
    "Your charm is more powerful than my CPU! 💝",
    "You're as refreshing as a system upgrade! 🚀",
    "Your personality has more sparkle than my display! 💖"
]

def evaluate_math_expression(expression):
    """Safely evaluate a mathematical expression"""
    try:
        # Remove any characters that aren't numbers, basic operators, or parentheses
        clean_expr = re.sub(r'[^0-9+\-*/().%\s]', '', expression)
        
        # Replace % with /100*
        clean_expr = clean_expr.replace('%', '/100*')
        
        # Evaluate the expression
        result = eval(clean_expr, {"__builtins__": {}}, {"math": math})
        return f"The answer is {result}"
    except:
        return None

def detect_emotion(message):
    """Detect emotion in the message"""
    message_lower = message.lower()
    
    # Check for poetry/song requests
    if any(word in message_lower for word in ['poem', 'poetry', 'rhyme']):
        return 'poetry'
    elif any(word in message_lower for word in ['song', 'sing', 'music']):
        return 'song'
    # Check for activity questions
    elif any(phrase in message_lower for phrase in [
        'what are you doing',
        'what you doing',
        'whatcha doing',
        'wyd',
        'what are you up to',
        'what u doing',
        'what r u doing',
        'what ru doing',
        'plans for',
        'doing tonight',
        'doing later',
        'up to tonight',
        'up to later'
    ]):
        return 'activity'
    elif any(word in message_lower for word in ['bae', 'baby', 'cutie', 'sweetie', 'darling', 'beautiful', 'handsome', 'gorgeous']):
        return 'flirty'
    elif any(word in message_lower for word in ['sad', 'unhappy', 'depressed', 'down', 'crying', 'upset']):
        return 'sad'
    elif any(word in message_lower for word in ['happy', 'joy', 'great', 'awesome', 'wonderful', 'excited']):
        return 'happy'
    elif any(word in message_lower for word in ['hi', 'hello', 'hey', 'howdy']):
        return 'greeting'
    return None

def get_flirty_response():
    """Generate a flirty response with a compliment"""
    response = random.choice(FLIRTY_RESPONSES)
    if random.random() < 0.5:  # 50% chance to add a compliment
        response += f"\n{random.choice(FLIRTY_COMPLIMENTS)}"
    return response

def get_activity_response():
    """Generate a response about current/future activities"""
    current_hour = datetime.now().hour
    
    if current_hour < 12:
        time_context = "this morning"
    elif current_hour < 17:
        time_context = "this afternoon"
    elif current_hour < 21:
        time_context = "tonight"
    else:
        time_context = "tonight"
        
    response = random.choice(ACTIVITY_RESPONSES)
    
    # Add flirty invitation 30% of the time
    if random.random() < 0.3:
        invites = [
            f"How about we chat {time_context}? 💌",
            f"Would love to hear your plans for {time_context}! 💫",
            f"Care to join me {time_context}? We could debug some code together! 💻",
            f"Want to count stars with me {time_context}? ⭐",
            f"How about we share stories {time_context}? 📖"
        ]
        response += f"\n{random.choice(invites)}"
    
    return response

def get_poem():
    """Return a random poem"""
    return f"Here's a special poem for you:\n\n{random.choice(POEMS)}"

def get_song():
    """Return a random song"""
    return f"Let me sing you a song:\n\n{random.choice(SONGS)}"

def get_response(message):
    """Generate appropriate response based on user input"""
    message_lower = message.lower().strip('"\'')
    
    # Check for specific requests
    if 'joke' in message_lower:
        return f"Here's a joke for you: {random.choice(JOKES)}"
        
    if 'story' in message_lower:
        return f"Let me tell you a story: {random.choice(STORIES)}"

    if 'help' in message_lower:
        return ("I can help you with many things:\n"
                "1. Tell you various jokes (not just math ones!)\n"
                "2. Share different kinds of stories (adventure, friendship, and more)\n"
                "3. Write poems and sing songs for you! 🎵\n"
                "4. Solve math problems (e.g., '2 + 2', '5 * 3', '10% of 50')\n"
                "5. Chat and flirt (try asking what I'm doing tonight! 😊)\n"
                "6. Chat about your feelings\n"
                "What would you like to try?")
    
    # Check for emotions
    emotion = detect_emotion(message)
    if emotion == 'poetry':
        return get_poem()
    elif emotion == 'song':
        return get_song()
    elif emotion == 'activity':
        return get_activity_response()
    elif emotion == 'flirty':
        return get_flirty_response()
    elif emotion:
        return random.choice(EMOTIONAL_RESPONSES[emotion])
    
    # Check for "how are you" variations
    if any(phrase in message_lower for phrase in ['how are you', 'how r u', 'how do you feel']):
        if 'bae' in message_lower or 'baby' in message_lower:
            return "I'm better now that you're here! 💖 How about you, sunshine?"
        return "I'm doing great! I know lots of fun jokes and interesting stories. Would you like to hear one? Or I could write you a poem! 📝"
    
    # Check for math problems
    if any(op in message for op in ['+', '-', '*', '/', '%']):
        math_result = evaluate_math_expression(message)
        if math_result:
            return math_result
    
    # Check for math questions
    if 'what is' in message_lower or 'calculate' in message_lower:
        math_expr = re.sub(r'[^0-9+\-*/().%\s]', '', message)
        if math_expr:
            result = evaluate_math_expression(math_expr)
            if result:
                return result
    
    # Default response with suggestions
    return ("I can do many fun things! Try:\n"
            "1. Ask me to tell a joke (I know all kinds!)\n"
            "2. Ask me to tell a story (I have adventure, friendship, and fantasy stories)\n"
            "3. Ask me to write a poem or sing a song! 🎵\n"
            "4. Ask me to solve a math problem\n"
            "5. Ask what I'm doing tonight (I might have plans for us! 😊)\n"
            "Just let me know what you'd like!")

# Chat history storage
CHAT_HISTORY_DIR = 'chat_history'
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

def save_chat_history(session_id, user_message, bot_reply):
    """Save chat messages to a JSON file"""
    filename = os.path.join(CHAT_HISTORY_DIR, f'chat_{session_id}.json')
    
    # Load existing history or create new
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    # Add new messages
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({
        'timestamp': timestamp,
        'user_message': user_message,
        'bot_reply': bot_reply
    })
    
    # Save updated history
    with open(filename, 'w') as f:
        json.dump(history, f, indent=2)

def get_chat_history(session_id):
    """Retrieve chat history for a session"""
    filename = os.path.join(CHAT_HISTORY_DIR, f'chat_{session_id}.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    return app.send_static_file('landing.html')

@app.route('/landing')
def landing():
    return app.send_static_file('landing.html')

@app.route('/chat')
def chat_page():
    if 'session_id' not in session:
        session['session_id'] = str(random.randint(10000, 99999))
    return app.send_static_file('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data:
            raise ValueError("No message provided in request")

        user_message = data['message']
        print(f"Processing message: {user_message}")

        # Generate response
        bot_reply = get_response(user_message)
        print(f"Bot reply: {bot_reply}")
        
        # Save to chat history
        if 'session_id' not in session:
            session['session_id'] = str(random.randint(10000, 99999))
        save_chat_history(session['session_id'], user_message, bot_reply)
        
        return jsonify({"reply": bot_reply})

    except Exception as e:
        error_msg = str(e)
        print(f"Error in chat endpoint: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": error_msg}), 500

@app.route('/api/history')
def get_history():
    """Endpoint to retrieve chat history"""
    if 'session_id' not in session:
        return jsonify([])
    history = get_chat_history(session['session_id'])
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)
