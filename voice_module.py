import queue
import threading
from dataclasses import dataclass
from typing import Callable, Optional

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover - optional dependency
    sr = None

try:
    import pyttsx3
except Exception:  # pragma: no cover - optional dependency
    pyttsx3 = None


@dataclass
class VoiceConfig:
    enable_input: bool = True
    enable_output: bool = True
    language: str = "en-US"
    # Shorter ambient calibration to reduce startup latency
    ambient_adjust_seconds: float = 0.5
    # Maximum time to wait for speech to start
    phrase_timeout: Optional[float] = 3.0
    # Maximum length of a single spoken phrase
    phrase_time_limit: Optional[float] = 6.0
    # Prefer offline recognition (PocketSphinx) when available
    prefer_offline: bool = True


class VoiceModule:
    """
    Production-oriented voice I/O wrapper.

    - Non-blocking background listening using a dedicated thread
    - Graceful handling of missing audio dependencies / hardware
    - Text-to-speech with interruptible playback
    - Simple callbacks for delivering recognized text back to the GUI / agent
    """

    def __init__(self, config: Optional[VoiceConfig] = None) -> None:
        self.config = config or VoiceConfig()

        self._recognizer = sr.Recognizer() if (sr and self.config.enable_input) else None
        self._microphone = sr.Microphone() if (sr and self.config.enable_input) else None

        self._tts_engine = pyttsx3.init() if (pyttsx3 and self.config.enable_output) else None
        self._tts_lock = threading.Lock()

        self._listening_thread: Optional[threading.Thread] = None
        self._listening_stop_event = threading.Event()
        self._result_queue: "queue.Queue[str]" = queue.Queue()
        self._callback: Optional[Callable[[str], None]] = None

        # Make recognition a bit more stable in noisy rooms
        if self._recognizer:
            self._recognizer.dynamic_energy_threshold = True
            self._recognizer.pause_threshold = 0.6

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def input_available(self) -> bool:
        """Return True if audio input is configured and ready."""
        return bool(self._recognizer and self._microphone)

    def start_listening(self, callback: Callable[[str], None]) -> None:
        """
        Start background listening and deliver recognized phrases via callback.
        Safe to call multiple times; subsequent calls restart the listener.
        """
        self._callback = callback
        if not self.input_available:
            # Voice input disabled or dependencies missing
            return

        self.stop_listening()

        self._listening_stop_event.clear()
        self._listening_thread = threading.Thread(
            target=self._listening_loop,
            name="VoiceModuleListener",
            daemon=True,
        )
        self._listening_thread.start()

    def stop_listening(self) -> None:
        """Stop background listening thread if running."""
        if self._listening_thread and self._listening_thread.is_alive():
            self._listening_stop_event.set()
            self._listening_thread.join(timeout=2.0)
        self._listening_thread = None

    def speak(self, text: str) -> None:
        """
        Convert text to speech.
        Returns immediately; TTS runs in a short-lived background thread.
        """
        if not text or not self._tts_engine:
            return

        def _run():
            with self._tts_lock:
                try:
                    self._tts_engine.stop()
                    self._tts_engine.say(text)
                    self._tts_engine.runAndWait()
                except Exception:
                    # TTS failures should not crash the app
                    pass

        threading.Thread(target=_run, name="VoiceModuleTTS", daemon=True).start()

    def get_pending_text(self) -> Optional[str]:
        """
        Non-blocking retrieval of the next recognized phrase.
        Mostly useful for testing; the GUI will typically rely on callbacks.
        """
        try:
            return self._result_queue.get_nowait()
        except queue.Empty:
            return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _listening_loop(self) -> None:
        assert self._recognizer and self._microphone

        try:
            with self._microphone as source:
                try:
                    self._recognizer.adjust_for_ambient_noise(
                        source, duration=self.config.ambient_adjust_seconds
                    )
                except Exception as exc:
                    # If calibration fails, continue with defaults instead of crashing
                    print(f"[VoiceModule] Ambient noise calibration failed: {exc}")

                while not self._listening_stop_event.is_set():
                    try:
                        # Some versions of SpeechRecognition may not support
                        # phrase_time_limit; fall back gracefully if needed.
                        try:
                            audio = self._recognizer.listen(
                                source,
                                timeout=self.config.phrase_timeout,
                                phrase_time_limit=self.config.phrase_time_limit,
                            )
                        except TypeError:
                            audio = self._recognizer.listen(
                                source,
                                timeout=self.config.phrase_timeout,
                            )
                    except Exception as exc:
                        if self._listening_stop_event.is_set():
                            break
                        print(f"[VoiceModule] Listening error: {exc}")
                        continue

                    try:
                        if self.config.prefer_offline:
                            # Try offline first (PocketSphinx); if it fails,
                            # fall back to the default Google recognizer.
                            try:
                                text = self._recognizer.recognize_sphinx(
                                    audio, language=self.config.language
                                )
                            except Exception as offline_exc:
                                print(f"[VoiceModule] Offline recognition failed: {offline_exc}")
                                text = self._recognizer.recognize_google(
                                    audio, language=self.config.language
                                )
                        else:
                            text = self._recognizer.recognize_google(
                                audio, language=self.config.language
                            )
                    except Exception as exc:
                        print(f"[VoiceModule] Recognition error: {exc}")
                        continue

                    text = text.strip()
                    if not text:
                        continue

                    self._result_queue.put(text)
                    if self._callback:
                        try:
                            self._callback(text)
                        except Exception:
                            # Guard the listener from GUI / agent errors
                            pass
        finally:
            self._listening_stop_event.set()

