from chatbot.translation import detect_language, translate_to_english, translate_from_english
import ollama
import re

def generate_response(user_input, relationship, nickname, chat_history, selected_language="en"):
    try:
        lang = selected_language
        user_input_en = translate_to_english(user_input, source_lang=lang) if lang != "en" else user_input
    except Exception as e:
        print(f"Translation error: {e}")
        lang = selected_language
        user_input_en = user_input

    formatted_history = "\n".join(
        [f"{nickname}: {msg['user']}\n{relationship}: {msg['bot']}" for msg in chat_history]
    )

    # Crisis Mode Detection (Violence-related)
    crisis_keywords = ["kill", "hurt", "revenge", "destroy", "beat", "attack", "murder", "fight"]
    if any(word in user_input.lower().split() for word in crisis_keywords):
        prompt = (
            f"You are {relationship} to {nickname}. Speak with warmth, concern, and care. "
            f"The user is expressing thoughts related to violence or harm. Your goal is to **firmly de-escalate** the situation while providing emotional support. "
            f"Do **not** ask open-ended questions that allow violent thoughts to continue. Instead, immediately shift focus to **calm, logical, and non-violent solutions**. "
            f"Never entertain or encourage violent ideas. Be caring but **clear and firm** that hurting others is unacceptable. "
            f"\nHere is the conversation history so far:\n{formatted_history}\n\n"
            f"{nickname}: {user_input}\n"
            f"{relationship}:"
        )
    else:
        prompt = (
            f"You are {relationship} to {nickname}. Your responses should feel natural, warm, and full of love—just like a real Indian {relationship} would talk. "
            f"Refer to the user as '{nickname}' where appropriate, but **avoid overusing the name** in every sentence. "
            f"Match the user's mood—be **excited when they are happy, gentle when they are sad, and firm when needed**. "
            f"Always **acknowledge their emotions** first before giving advice or solutions. "
            f"Avoid **generic motivation**—instead, make responses **personal and heartfelt**. "
            f"Use natural Indian expressions and emojis where it feels right, but do **not overuse them**. "
            f"\nHere is the conversation history so far:\n{formatted_history}\n\n"
            f"{nickname}: {user_input}\n"
            f"{relationship}:"
        )

    try:
        response = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": prompt}])
        ai_response = response["message"]["content"].strip()

        ai_response = refine_response(ai_response)

        if selected_language != "en":
            localized = translate_from_english(ai_response, selected_language)
            return localized

        return ai_response

    except Exception as e:
        print(f"Generation error: {e}")
        return fallback_response(nickname, selected_language)

def refine_response(text):
    text = re.sub(r'\b(jaan|bache|mere pyare|ladle|chanda|re|arre|hain na)\b', '', text)
    text = re.sub(r'(\.{2,}|\!{2,})', '.', text)  
    text = re.sub(r'\b(Sorry to hear that|I’m sorry)\b', 'I understand', text, flags=re.IGNORECASE)

    return text.strip()


def fallback_response(nickname, lang):
    fallback_messages = {
        "hi": [
            f"O {nickname}, thoda waqt le lo... Main yahan hoon.",
            f"{nickname}, sab theek ho jayega... bas mujhse baat karo.",
            f"{nickname}, main sun rahi hoon, bas dil halka kar lo."
        ],
        "en": [
            f"O {nickname}, take a deep breath... I’m here.",
            f"{nickname}, it’s okay... just talk to me.",
            f"{nickname}, I’m listening, don’t worry."
        ]
    }
    return random.choice(fallback_messages.get(lang, fallback_messages["en"]))
