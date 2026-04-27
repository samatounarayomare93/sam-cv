import os
import logging
import asyncio

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [VOICE OPS] - %(message)s")

# --- Graceful imports: these libraries may not be available on cloud (Render) ---
sr = None
AudioSegment = None

try:
    import speech_recognition as sr
except ImportError:
    logging.warning("⚠️ SpeechRecognition not installed. Voice transcription disabled.")

try:
    from pydub import AudioSegment
except ImportError:
    logging.warning("⚠️ pydub not installed. Audio conversion disabled.")

from telegram import Update
from telegram.ext import ContextTypes


class VoiceCommander:
    """
    Zero-Cost Interview Copilot.
    Downloads voice notes from Telegram, converts OGG→WAV via pydub/ffmpeg,
    and transcribes via Google Free Web Speech API.
    Requires ffmpeg on PATH for conversion.
    """

    def __init__(self, dispatch_callback):
        """
        dispatch_callback: SovereignDashboard._dispatch_command
        Allows triggering /run, /status, etc. directly from voice.
        """
        self.dispatch_callback = dispatch_callback
        if sr is not None:
            self.r = sr.Recognizer()
        else:
            self.r = None

    @property
    def is_available(self) -> bool:
        return sr is not None and AudioSegment is not None

    async def handle_voice_note(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Downloads Telegram Voice Note (.ogg), converts to .wav, and transcribes."""
        voice = update.message.voice
        if not voice:
            return

        if not self.is_available:
            await update.message.reply_text(
                "⚠️ <b>Voice Ops Offline.</b>\n"
                "SpeechRecognition / pydub libraries not available in this environment.\n"
                "<i>Install: pip install SpeechRecognition pydub</i>\n"
                "<i>Also ensure ffmpeg is on your PATH.</i>",
                parse_mode='HTML'
            )
            return

        logging.info("🎙️ Voice Note Received. Engaging Zero-Cost Transcriber...")

        file = await context.bot.get_file(voice.file_id)
        ogg_path = f"voice_{voice.file_id}.ogg"
        wav_path = f"voice_{voice.file_id}.wav"

        await file.download_to_drive(ogg_path)

        try:
            # Convert OGG → WAV using pydub (requires ffmpeg on PATH)
            audio = AudioSegment.from_ogg(ogg_path)
            audio.export(wav_path, format="wav")

            # Transcribe using zero-cost Google Web Speech API
            with sr.AudioFile(wav_path) as source:
                audio_data = self.r.record(source)
                try:
                    text = self.r.recognize_google(audio_data).lower()
                    logging.info(f"🗣️ Transcribed: '{text}'")

                    await update.message.reply_text(
                        f"🗣️ <b>Voice Command Registered:</b> <code>{text}</code>",
                        parse_mode='HTML'
                    )

                    # Map spoken words → dashboard commands
                    if any(w in text for w in ["run", "launch", "start", "attack", "strike"]):
                        await self.dispatch_callback("/launch_infinite", update, context)
                    elif any(w in text for w in ["status", "how are you", "health", "report"]):
                        await self.dispatch_callback("/status", update, context)
                    elif any(w in text for w in ["stop", "halt", "pause", "freeze"]):
                        await self.dispatch_callback("/pause", update, context)
                    elif any(w in text for w in ["resume", "continue", "go", "proceed"]):
                        await self.dispatch_callback("/resume", update, context)
                    elif any(w in text for w in ["reboot", "restart", "reset"]):
                        await self.dispatch_callback("/reboot", update, context)
                    elif any(w in text for w in ["stats", "statistics", "numbers", "count"]):
                        await self.dispatch_callback("/stats", update, context)
                    elif any(w in text for w in ["oracle", "market", "leads", "news"]):
                        await self.dispatch_callback("/oracle", update, context)
                    elif any(w in text for w in ["interview", "prep", "cheat sheet", "ghost"]):
                        await self.dispatch_callback("/mock_interview", update, context)
                    elif any(w in text for w in ["backup", "save", "archive"]):
                        await self.dispatch_callback("/backup", update, context)
                    else:
                        await update.message.reply_text(
                            "⚠️ <b>Voice Oracle:</b> Command not recognized.\n"
                            "<i>Try saying: run, status, pause, resume, stats, reboot, backup</i>",
                            parse_mode='HTML'
                        )

                except sr.UnknownValueError:
                    await update.message.reply_text(
                        "🔇 <b>Voice Oracle:</b> Could not decipher audio. Speak clearly and closer to the mic.",
                        parse_mode='HTML'
                    )
                except sr.RequestError as e:
                    await update.message.reply_text(
                        f"⚠️ <b>Voice API Error:</b> {e}\n<i>Check internet connection.</i>",
                        parse_mode='HTML'
                    )

        except FileNotFoundError:
            await update.message.reply_text(
                "⚠️ <b>Voice Protocol Failed:</b> `ffmpeg` is not installed or not on PATH.\n"
                "<i>Install: https://ffmpeg.org/download.html</i>",
                parse_mode='HTML'
            )
        except Exception as e:
            logging.error(f"Voice Processing Error: {e}")
            await update.message.reply_text(
                f"⚠️ <b>Voice Protocol Error:</b> {e}",
                parse_mode='HTML'
            )
        finally:
            # Cleanup temp files
            for path in [ogg_path, wav_path]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception:
                        pass
