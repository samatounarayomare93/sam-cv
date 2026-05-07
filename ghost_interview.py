import os
import asyncio
import logging
from logging import INFO
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv

# Initialize
load_dotenv()
logging.basicConfig(level=INFO, format="%(asctime)s - [GHOST WHISPERER] - %(message)s")

# ZERO-COST REQUIREMENT: Uses Gemini Free Tier
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# [🛡️ FIX 2026-05-07]: gemini-2.0-flash-exp deprecated → use gemini-2.5-flash
model = genai.GenerativeModel('gemini-2.5-flash')

def test_microphone():
    """Identify Stereo Mix or primary mic."""
    logging.info("Available Audio Devices:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        logging.info(f"[{index}] {name}")
        
async def generate_tactical_response(transcription: str):
    """Feeds HR questions to Gemini for an instant HR Operations answer."""
    logging.info(f"Target Asked (Transcribed): '{transcription}'")
    
    prompt = f"""
    You are an elite, God-Tier HR Operations Director. You are currently in a live Zoom interview.
    The HR Manager just asked you the following question: 
    "{transcription}"
    
    Provide an immediate, highly tactical, brilliant response that proves you are a top-tier HR Operations expert.
    Do not use introductory filler (like 'Here is a response:'). 
    Keep it under 3 sentences. Be authosamtive, data-driven, and confident.
    """
    
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        print("\n" + "="*60)
        print("👑 GHOST WHISPERER TACTICAL RESPONSE:")
        print(response.text.strip())
        print("="*60 + "\n")
    except Exception as e:
        logging.error(f"LLM Error: {e}")

def listen_loop():
    """Continuous local audio capture using zero-cost SpeechRecognition."""
    r = sr.Recognizer()
    
    # NOTE: Set device_index to your 'Stereo Mix' index if you want to capture Zoom. 
    # Otherwise, it uses the default microphone.
    with sr.Microphone() as source:
        logging.info("Calibrating background noise... (Please wait 2 seconds)")
        r.adjust_for_ambient_noise(source, duration=2)
        logging.info("🎙️ Ghost Whisperer is LIVE. Listening to system audio...")
        
        while True:
            try:
                # Listen for chunks of speech
                audio = r.listen(source, timeout=5, phrase_time_limit=15)
                # ZERO-COST: Using Google's FREE web speech API (No API key required)
                text = r.recognize_google(audio)
                
                if len(text.split()) > 3: # Only process meaningful sentences
                    asyncio.run(generate_tactical_response(text))
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                # Could not understand audio
                continue
            except sr.RequestError as e:
                logging.error(f"Could not request results from Google Speech service; {e}")
            except KeyboardInterrupt:
                logging.info("Ghost Whisperer shutting down.")
                break

if __name__ == "__main__":
    print("""
    ================================================================
    👻 GHOST WHISPERER (ZERO-COST INTERVIEW COPILOT) 👻
    Requirement: To capture Zoom/Teams, ensure "Stereo Mix" is enabled
    in Windows Sound Control Panel and set as Default Recording Device.
    ================================================================
    """)
    listen_loop()
