import sounddevice as sd
import numpy as np
import speech_recognition as sr

""" если не требуется, то "#" - def print wasapi devices """
def print_wasapi_devices():
    devices = sd.query_devices()
    wasapi_api_indices = [i for i, h in enumerate(sd.query_hostapis()) if h['name'] == 'Windows WASAPI']

    if not wasapi_api_indices:
        print("WASAPI не найден. Убедитесь, что вы работаете на Windows.")
        return

    wasapi_api_index = wasapi_api_indices[0]

    print("Доступные устройства с поддержкой WASAPI:")
    for idx, dev in enumerate(devices):
        if dev['hostapi'] == wasapi_api_index:
            print(f"ID: {idx}, Name: {dev['name']}, Max Output Channels: {dev['max_output_channels']}, Max Input Channels: {dev['max_input_channels']}")

def list_output_devices():
    """Возвращает список устройств вывода звука, поддерживающих loopback"""
    devices = sd.query_devices()
    output_devices = {}
    wasapi_hostapis = [i for i, h in enumerate(sd.query_hostapis()) if h['name'] == 'Windows WASAPI']

    if not wasapi_hostapis:
        print("WASAPI не найден. Убедитесь, что вы работаете на Windows.")
        return output_devices

    wasapi_api_index = wasapi_hostapis[0]

    for i, dev in enumerate(devices):
        if dev["max_output_channels"] > 0 and dev["hostapi"] == wasapi_api_index:
            output_devices[i] = dev["name"]
    return output_devices

def get_audio_level(device_index, sample_rate=48000):
    """Возвращает уровень громкости звука с устройства вывода"""
    try:
        wasapi_info = sd.WasapiSettings(exclusive=False)
        wasapi_info.loopback = True

        device_info = sd.query_devices(device_index, 'output')
        channels = int(device_info['max_output_channels'])
        print(f"Устройство '{device_info['name']}' поддерживает {channels} каналов вывода.")

        sd.check_input_settings(device=device_index, channels=channels, samplerate=sample_rate,
                                extra_settings=wasapi_info)

        with sd.InputStream(device=device_index, channels=channels, samplerate=sample_rate,
                            extra_settings=wasapi_info) as stream:
            data, _ = stream.read(1024)
            volume_norm = np.linalg.norm(data) * 10
            return int(volume_norm)
    except Exception as e:
        print(f"🚨 Ошибка получения уровня звука: {e}")
        return 0


def capture_audio_from_output(device_index, duration=5, sample_rate=48000):
    """Записывает звук с выхода (динамиков)"""
    try:
        wasapi_info = sd.WasapiSettings(exclusive=False)
        wasapi_info.loopback = True

        device_info = sd.query_devices(device_index, 'output')
        channels = int(device_info['max_output_channels'])
        print(f"Устройство '{device_info['name']}' поддерживает {channels} каналов вывода.")

        sd.check_input_settings(device=device_index, channels=channels, samplerate=sample_rate,
                                extra_settings=wasapi_info)

        with sd.InputStream(device=device_index, channels=channels, samplerate=sample_rate, dtype='int16',
                            extra_settings=wasapi_info) as stream:
            audio_data = stream.read(int(duration * sample_rate))[0]
        sd.wait()

        recognizer = sr.Recognizer()
        audio = sr.AudioData(audio_data.tobytes(), sample_rate, channels)

        try:
            return recognizer.recognize_google(audio, language="ru-RU")
        except sr.UnknownValueError:
            return "⚠ Не удалось распознать речь"
        except sr.RequestError:
            return "⚠ Ошибка запроса к Google API"
    except Exception as e:
        return f"🚨 Ошибка: {e}"


""" print - def print_wasapi_devices(): """
if __name__ == '__main__':
    print_wasapi_devices()