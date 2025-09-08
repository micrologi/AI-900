#pip install azure-cognitiveservices-speech
import sys
import threading
import time
from typing import List
from dotenv import load_dotenv
import os

load_dotenv('.env')

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError as e:
    print("\n[ERRO] Precisa instalar o SDK: pip install azure-cognitiveservices-speech\n")
    raise

SOURCE_LANG_CANDIDATES: List[str] = [
    "pt-BR",  # Português (Brasil)
    "en-US",  # Inglês (EUA)
    "es-ES",  # Espanhol (Espanha) – ajuste para es-MX se preferir
]

# Traduções de texto que você quer ver no console (códigos ISO-639, sem região)
TARGET_TEXT_LANGS: List[str] = [
    "en",     # Inglês
    "pt",     # Português
]

# Idioma que será FALADO (TTS) – escolha um dos acima
SPOKEN_TARGET: str = "en"  # "en" ou "pt"

# Vozes sugeridas (mude se quiser outras):
VOICE_BY_LANG = {
    "en": "en-US-AriaNeural",
    "pt": "pt-BR-FranciscaNeural",
}

# ===============================================

def build_translation_config() -> speechsdk.translation.SpeechTranslationConfig:
    speech_region = os.getenv('region')
    speech_key = os.getenv("key")

    config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key,
        region=speech_region,
    )

    # (Opcional) Melhorias de reconhecimento
    # config.set_profanity(speechsdk.ProfanityOption.Raw)

    # Adiciona idiomas de destino para tradução de TEXTO
    for lang in TARGET_TEXT_LANGS:
        config.add_target_language(lang)

    # Define voz/idioma para FALAR a tradução principal
    voice = VOICE_BY_LANG.get(SPOKEN_TARGET)
    if voice:
        config.speech_synthesis_voice_name = voice

    return config


def build_recognizer(config: speechsdk.translation.SpeechTranslationConfig) -> speechsdk.translation.TranslationRecognizer:
    # Entrada: microfone padrão
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Detecção automática do idioma de origem
    auto_lang_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=SOURCE_LANG_CANDIDATES
    )

    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=config,
        auto_detect_source_language_config=auto_lang_config,
        audio_config=audio_config,
    )
    return recognizer


def build_synthesizer_from_config(config: speechsdk.translation.SpeechTranslationConfig) -> speechsdk.SpeechSynthesizer:
    # Saída: alto-falante padrão
    out_audio = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_key = os.getenv("key")
    speech_region = os.getenv('region')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

    voice = VOICE_BY_LANG.get(SPOKEN_TARGET)
    if voice:
        speech_config.speech_synthesis_voice_name = voice

    return speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=out_audio)


class GracefulStop:

    def __init__(self) -> None:
        self._stop = False

    @property
    def stopped(self) -> bool:
        return self._stop

    def request_stop(self) -> None:
        self._stop = True


def main():
    print("\n=== Tradutor de Tempo Real – Azure AI Speech ===")
    print("Pressione Ctrl+C para parar.\n")

    config = build_translation_config()
    recognizer = build_recognizer(config)
    synthesizer = build_synthesizer_from_config(config)

    stopper = GracefulStop()

    # ---- Handlers de eventos (parciais e finais) ----
    def recognizing(evt: speechsdk.translation.TranslationRecognitionEventArgs):
        # Parciais: mostram a transcrição e a(s) tradução(ões) provisórias
        text = evt.result.text
        translations = evt.result.translations or {}
        parts = []
        if text:
            parts.append(f"orig: {text}")
        for lang, t in translations.items():
            parts.append(f"{lang}(~): {t}")
        if parts:
            print("\r" + "  ".join(parts)[:120], end="")  # linha única (preview)

    def recognized(evt: speechsdk.translation.TranslationRecognitionEventArgs):
        # Finais: imprime limpo e fala a tradução principal
        if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
            # Limpa a linha anterior
            print("\r" + " " * 140, end="\r")

            src_text = evt.result.text
            translations = dict(evt.result.translations)
            print("▶", src_text)
            for lang in TARGET_TEXT_LANGS:
                if lang in translations:
                    print(f"  → {lang}: {translations[lang]}")

            # Falar a tradução no idioma escolhido
            spoken = translations.get(SPOKEN_TARGET)
            if spoken:
                _ = synthesizer.speak_text_async(spoken).get()
                
        elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # Sem tradução disponível (pode ocorrer se target não suportado)
            print(f"(Reconhecido, sem tradução) {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("[NoMatch] Não foi possível reconhecer/ traduzir.")

    def canceled(evt: speechsdk.translation.TranslationRecognitionCanceledEventArgs):
        print(f"[Cancelado] Motivo: {evt.reason}; Detalhes: {evt.error_details}")
        stopper.request_stop()

    def session_started(evt):
        print("[Sessão] iniciada.")

    def session_stopped(evt):
        print("[Sessão] encerrada.")
        stopper.request_stop()

    recognizer.recognizing.connect(recognizing)
    recognizer.recognized.connect(recognized)
    recognizer.canceled.connect(canceled)
    recognizer.session_started.connect(session_started)
    recognizer.session_stopped.connect(session_stopped)

    # ---- Inicia reconhecimento contínuo ----
    recognizer.start_continuous_recognition()

    try:
        while not stopper.stopped:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nParando…")
    finally:
        recognizer.stop_continuous_recognition()


if __name__ == "__main__":
    main()
