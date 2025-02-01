import sounddevice as sd
import numpy as np
import speech_recognition as sr

def list_output_devices():
    """Возвращает список доступных устройств вывода звука"""
    devices = sd.query_devices()
    return {i: dev["name"] for i, dev in enumerate(devices) if dev["max_output_channels"] > 0}

def get_audio_level(device_index, sample_rate=44100):
    """Возвращает уровень громкости звука с устройства вывода"""
    try:
        with sd.InputStream(device=device_index, channels=1, samplerate=sample_rate) as stream:
            data, _ = stream.read(1024)
            volume_norm = np.linalg.norm(data) * 10
            return int(volume_norm)  # Приводим уровень к целому числу
    except Exception as e:
        print(f"🚨 Ошибка получения уровня звука: {e}")
        return 0

def capture_audio_from_output(device_index, duration=5, sample_rate=44100):
    """Записывает звук с выхода (динамиков)"""
    try:
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate,
                            channels=1, dtype=np.int16, device=device_index)
        sd.wait()

        recognizer = sr.Recognizer()
        audio = sr.AudioData(audio_data.tobytes(), sample_rate, 1)

        try:
            return recognizer.recognize_google(audio, language="ru-RU")
        except sr.UnknownValueError:
            return "⚠ Не удалось распознать речь"
        except sr.RequestError:
            return "⚠ Ошибка запроса к Google API"
    except Exception as e:
        return f"🚨 Ошибка: {e}"
