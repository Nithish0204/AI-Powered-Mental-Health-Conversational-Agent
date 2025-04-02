from deep_translator import GoogleTranslator
import langid
import logging
import re


langid.set_languages(['en', 'hi']) 

def detect_language(text):
    """Improved Hindi detection with multiple checks"""
    try:
        
        devanagari_chars = re.compile(r'[\u0900-\u097F]')
        if devanagari_chars.search(text):
            return 'hi'
            
        hindi_roman_keywords = ['maa', 'beta', 'shukriya', 'achha']
        if any(word in text.lower() for word in hindi_roman_keywords):
            return 'hi'
            
        lang, confidence = langid.classify(text)
        if confidence > 0.85:
            return lang

        if len(text.split()) < 5:
            return 'en'
            
        return 'en'  
    except Exception as e:
        logging.error(f"Detection error: {str(e)}")
        return 'en'

def translate_to_english(text, source_lang=None):
    try:

        if source_lang and source_lang != 'en':
            return GoogleTranslator(source=source_lang, target='en').translate(text)
            
        detected_lang = detect_language(text)
        if detected_lang != 'en':
            return GoogleTranslator(source=detected_lang, target='en').translate(text)
            
        return text
    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        return text

def translate_from_english(text, target_lang):
    try:
        detected_lang = detect_language(text)
        if detected_lang == target_lang:
            return text  

        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        if target_lang == 'hi':
            return translated.replace('?', '? ').replace('.', '। ') 
        return translated
    except Exception as e:
        logging.error(f"Back-translation error: {str(e)}")
        return text
