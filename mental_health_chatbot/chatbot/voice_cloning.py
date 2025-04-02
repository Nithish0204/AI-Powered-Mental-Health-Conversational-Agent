import os
import requests
from dotenv import load_dotenv


load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def clone_voice(voice_path):
    """Sends the uploaded voice sample to ElevenLabs API for cloning."""
    
    url = "https://api.elevenlabs.io/v1/voices/add"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    files = {
        "files": open(voice_path, "rb")  
    }
    
    data = {
        "name": "UserClonedVoice" 
    }
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        voice_id = response.json().get("voice_id")  
        print(f"✅ Cloned voice successfully: {voice_id}")
        return voice_id  
    else:
        print(f"❌ Error cloning voice ({response.status_code}): {response.json()}") 
        return None