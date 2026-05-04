"""
AI Voice Assistant
Voice-controlled bot with speech recognition and text-to-speech
"""

import os
from typing import Dict, Any, List

class VoiceAssistant:
    """AI-powered voice assistant for the job bot"""
    
    def __init__(self):
        self.commands = {
            "status": ["status", "what's my status", "how am i doing", "show status"],
            "stats": ["stats", "statistics", "show stats", "my statistics"],
            "jobs": ["jobs", "show jobs", "new jobs", "latest jobs"],
            "applications": ["applications", "my applications", "show applications"],
            "help": ["help", "what can you do", "commands", "show commands"],
            "start": ["start", "begin", "start bot", "activate"],
            "stop": ["stop", "pause", "stop bot", "deactivate"],
            "test": ["test", "run test", "test bot"],
        }
        
        self.responses = {
            "greeting": "Hello! I'm your job search assistant. How can I help you today?",
            "status": "Let me check your status...",
            "stats": "Here are your statistics...",
            "jobs": "Fetching latest jobs for you...",
            "applications": "Loading your applications...",
            "help": "I can help you with: status, stats, jobs, applications, and more!",
            "unknown": "I didn't understand that. Try saying 'help' for available commands.",
            "goodbye": "Goodbye! Good luck with your job search!"
        }
    
    def process_voice_command(self, text: str) -> Dict[str, Any]:
        """Process voice command and return action"""
        
        text = text.lower().strip()
        
        # Match command
        for command, keywords in self.commands.items():
            if any(keyword in text for keyword in keywords):
                return {
                    "command": command,
                    "text": text,
                    "response": self.responses.get(command, self.responses["unknown"])
                }
        
        return {
            "command": "unknown",
            "text": text,
            "response": self.responses["unknown"]
        }
    
    def generate_voice_report(self, stats: Dict[str, Any]) -> str:
        """Generate voice-friendly report"""
        
        report = f"""
Here's your job search summary:

You have applied to {stats.get('total_applications', 0)} positions.

{stats.get('pending', 0)} applications are pending.
{stats.get('interviews', 0)} interview requests received.
{stats.get('offers', 0)} job offers received.

Your response rate is {stats.get('response_rate', 0)} percent.

You've discovered {stats.get('jobs_found', 0)} new jobs today.

Keep up the great work!
"""
        return report.strip()
    
    def text_to_speech_guide(self) -> str:
        """Guide for implementing text-to-speech"""
        
        return """
# 🎙️ Voice Assistant Implementation Guide

## Text-to-Speech (TTS)

### Option 1: Google Text-to-Speech (Free)
```python
from gtts import gTTS
import os

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("start response.mp3")  # Windows
    # os.system("afplay response.mp3")  # Mac
    # os.system("mpg321 response.mp3")  # Linux
```

### Option 2: pyttsx3 (Offline)
```python
import pyttsx3

engine = pyttsx3.init()
engine.say("Hello! I'm your job search assistant")
engine.runAndWait()
```

### Option 3: Azure Speech (Best Quality)
```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="YOUR_KEY",
    region="YOUR_REGION"
)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
synthesizer.speak_text_async("Hello!").get()
```

---

## Speech-to-Text (STT)

### Option 1: Google Speech Recognition (Free)
```python
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)
    print(f"You said: {text}")
```

### Option 2: Azure Speech (Best Accuracy)
```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="YOUR_KEY",
    region="YOUR_REGION"
)
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
result = recognizer.recognize_once()
print(f"You said: {result.text}")
```

---

## Voice Commands

### Available Commands:
- "Show my status"
- "What are my statistics?"
- "Show me new jobs"
- "List my applications"
- "Help"
- "Start the bot"
- "Stop the bot"

### Example Usage:
```python
from core.voice_assistant import VoiceAssistant

assistant = VoiceAssistant()

# Process command
result = assistant.process_voice_command("show my status")
print(result['response'])

# Generate voice report
stats = {"total_applications": 50, "pending": 30, "interviews": 5}
report = assistant.generate_voice_report(stats)
print(report)
```

---

## Installation

```bash
# For speech recognition
pip install SpeechRecognition pyaudio

# For text-to-speech
pip install gtts pyttsx3

# For Azure (optional, best quality)
pip install azure-cognitiveservices-speech
```

---

## Integration with Telegram

```python
# Voice messages in Telegram
from telegram import Update
from telegram.ext import MessageHandler, filters

async def handle_voice(update: Update, context):
    # Download voice message
    voice_file = await update.message.voice.get_file()
    await voice_file.download_to_drive('voice.ogg')
    
    # Convert to text
    text = speech_to_text('voice.ogg')
    
    # Process command
    result = assistant.process_voice_command(text)
    
    # Send response
    await update.message.reply_text(result['response'])

# Add handler
application.add_handler(MessageHandler(filters.VOICE, handle_voice))
```
"""


def get_voice_assistant():
    """Get voice assistant instance"""
    return VoiceAssistant()
