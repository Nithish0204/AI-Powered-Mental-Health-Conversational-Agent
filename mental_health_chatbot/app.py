from flask import Flask, render_template, request, jsonify, session, send_from_directory
from chatbot.translation import detect_language, translate_to_english, translate_from_english
from chatbot.response_generator import generate_response
from chatbot.speech_to_text import transcribe_audio
from chatbot.voice_cloning import clone_voice
import os
from dotenv import load_dotenv
import time
import requests
from textblob import TextBlob
import logging
import re

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
app_secret = os.getenv("FLASK_SECRET_KEY", "super_secret_key")

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = app_secret

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"
SUPPORTED_LANGUAGES = ['en', 'hi']  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

VOICE_MAPPINGS = {
    "relationship": {
        "mom": "NeDTo4pprKj2ZwuNJceH",
        "dad": "3gsg3cxXyFLcGIfNbM6C",
        "brother": "MF3mGyEYCl7XYWbV9V6O",
    },
    "gender": {
        "boy": "MF3mGyEYCl7XYWbV9V6O",
        "girl": "6BZyx2XekeeXOkTVn8un"
    }
}

def get_appropriate_tone(text):
    """Determine response tone based on sentiment"""
    try:
        analysis = TextBlob(text)
        if analysis.sentiment.polarity < -0.5:
            return "gentle and reassuring"
        elif analysis.sentiment.polarity < 0:
            return "compassionate and understanding"
        elif analysis.sentiment.polarity > 0.3:
            return "warm and cheerful"
        return "neutral and supportive"
    except:
        return "neutral and caring"

def analyze_sentiment(text):
    """Simple sentiment analysis for response handling"""
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return 0.0

def cleanup_old_files(directory, max_age=86400):
    current_time = time.time()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and (current_time - os.path.getmtime(filepath)) > max_age:
            try:
                os.remove(filepath)
                logging.info(f"Cleaned up: {filepath}")
            except Exception as e:
                logging.error(f"Cleanup error: {str(e)}")

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def handle_chat():
    try:
        cleanup_old_files(STATIC_FOLDER)
        cleanup_old_files(UPLOAD_FOLDER)

        selected_language = "en"
        if request.content_type.startswith('multipart/form-data'):
            selected_language = request.form.get("language", "en").lower()
        elif request.content_type == "application/json":
            data = request.get_json()
            selected_language = data.get("language", "en").lower()

        if selected_language not in SUPPORTED_LANGUAGES:
            selected_language = "en"

        user_message = ""
        relationship = ""
        nickname = ""
        gender = ""
        voice_id = session.get('cloned_voice_id')
        is_initial_setup = False


        if request.content_type.startswith('multipart/form-data'):
            if "audio" not in request.files:
                is_initial_setup = True
                relationship = request.form.get("relationship", "").lower().strip()
                nickname = request.form.get("nickname", "").strip()
                gender = request.form.get("gender", "").lower().strip()
                if "voice_sample" in request.files:
                    voice_sample = request.files["voice_sample"]
                    if voice_sample.filename:
                        voice_path = os.path.join(app.config["UPLOAD_FOLDER"], "voice_sample.wav")
                        voice_sample.save(voice_path)
                        cloned_voice_id = clone_voice(voice_path)
                        if cloned_voice_id:
                            session['cloned_voice_id'] = cloned_voice_id
                            voice_id = cloned_voice_id
            else:
                audio_file = request.files["audio"]
                if audio_file.filename == "":
                    return jsonify({"error": "Invalid audio file"}), 400
                
                audio_path = os.path.join(app.config["UPLOAD_FOLDER"], "voice_input.wav")
                audio_file.save(audio_path)
                user_message = transcribe_audio(audio_path) or ""
                
                relationship = request.form.get("relationship", "").lower().strip()
                nickname = request.form.get("nickname", "").strip()
                gender = request.form.get("gender", "").lower().strip()

        elif request.content_type == "application/json":
            data = request.get_json()
            user_message = data.get("message", "").strip()
            relationship = data.get("relationship", "").lower().strip()
            nickname = data.get("nickname", "").strip()
            gender = data.get("gender", "").lower().strip()

        if not relationship or not nickname:
            return jsonify({"error": "Relationship and nickname are required"}), 400
            
        if not is_initial_setup and not user_message:
            return jsonify({"error": "Empty message received"}), 400

        if is_initial_setup:
            bot_response = generate_welcome_message(relationship, nickname, selected_language)
            audio_url = generate_speech(bot_response, relationship, gender, voice_id, selected_language)
            
            return jsonify({
                "response": bot_response,
                "audio_url": f"/static/{os.path.basename(audio_url)}" if audio_url else "",
                "language": selected_language
            })

        chat_history = session.get("chat_history", [])
        try:
             bot_response = generate_response(
                user_message,  
                relationship,
                nickname,
                chat_history,
                selected_language=selected_language  
            )
        except Exception as e:
            logging.error(f"Response generation failed: {str(e)}")
            return jsonify({"error": "Failed to generate response"}), 500

        try:
            if selected_language != "en":
                bot_response = translate_from_english(bot_response, selected_language)

            bot_response = re.sub(r'\b(\w+)( \1)+\b', r'\1', bot_response)
            if selected_language == "hi":
                bot_response = bot_response.replace("..", "।").replace("?.", "?")
                if not bot_response.endswith((".", "!", "?", "।")):
                    bot_response += "।"
            else:
                bot_response = bot_response.replace(" but ", ", but ")
                if not bot_response.endswith((".", "!", "?")):
                    bot_response += "."

        except Exception as e:
            logging.error(f"Post-processing failed: {str(e)}")

        chat_history.append({"user": user_message, "bot": bot_response})
        session["chat_history"] = chat_history[-10:]

        audio_url = ""
        try:
            audio_path = generate_speech(bot_response, relationship, gender, voice_id, selected_language)
            if audio_path:
                audio_url = f"/static/{os.path.basename(audio_path)}"
        except Exception as e:
            logging.error(f"Speech generation failed: {str(e)}")

        return jsonify({
            "response": bot_response,
            "audio_url": audio_url,
            "language": selected_language
        })

    except Exception as e:
        logging.error(f"Chat processing error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    
def generate_welcome_message(relationship, nickname, language):
    """Culture-aware welcome messages"""
    greetings = {
        "en": f"Hello {nickname}! How are you feeling today?",
        "hi": f"नमस्ते {nickname}!  आज आप कैसा महसूस कर रहे हैं?",
        "es": f"Hola {nickname}! ¿Cómo te sientes hoy?",
        "de": f"Hallo {nickname}!  Wie fühlst du dich heute?"
    }
    return greetings.get(language, greetings["en"])


def generate_speech(text, relationship, gender, voice_id, language):
    """Generate speech with fallback handling"""
    try:
        voice_id = voice_id or \
            VOICE_MAPPINGS['relationship'].get(relationship) or \
            VOICE_MAPPINGS['gender'].get(gender) or \
            "NeDTo4pprKj2ZwuNJceH"

        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            },
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            timeout=10
        )

        if response.status_code == 200:
            filename = f"output_{int(time.time())}.mp3"
            audio_path = os.path.join(STATIC_FOLDER, filename)
            with open(audio_path, "wb") as f:
                f.write(response.content)
            return audio_path
            
        logging.error(f"Voice API error: {response.text}")
        return None
    except Exception as e:
        logging.error(f"Speech generation failed: {str(e)}")
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)