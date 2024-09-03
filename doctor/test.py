
import speech_recognition as sr
from googletrans import Translator
import google.generativeai as genai

# genai.configure(api_key="AIzaSyDdEVqEWK0INky4NT3dnLuFz88c-OQi6wU")
model = genai.GenerativeModel('gemini-pro')



recognizer = sr.Recognizer()
translator = Translator()
    # Load Hindi audio file (replace 'hindi_audio.wav' with your actual file)
with sr.AudioFile("D:\\rural\\sounds\\output.wav") as source:
    audio_data = recognizer.record(source)

    # Recognize speech from Hindi audio
    hindi_text = recognizer.recognize_google(audio_data, language='hi-IN')
    print("Hindi Text:", hindi_text)


        # Translate Hindi text to English
    english_translation = model.generate_content("translate to english"+hindi_text).text
    print("English Translation:", english_translation)

