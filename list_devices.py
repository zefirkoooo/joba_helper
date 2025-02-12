import sounddevice as sd


''' Доступные устройства '''

print("Доступные хост-API:")
for i, api in enumerate(sd.query_hostapis()):
    print(f"ID: {i}, Name: {api['name']}")

print("\nДоступные устройства:")
for i, dev in enumerate(sd.query_devices()):
    print(f"ID: {i}, Name: {dev['name']}, HostAPI: {sd.query_hostapis()[dev['hostapi']]['name']}")




# def print_wasapi_devices():
#     devices = sd.query_devices()
#     wasapi_api_indices = [i for i, h in enumerate(sd.query_hostapis()) if h['name'] == 'Windows WASAPI']
#
#     if not wasapi_api_indices:
#         print("WASAPI не найден. Убедитесь, что вы работаете на Windows.")
#         return
#
#     wasapi_api_index = wasapi_api_indices[0]
#
#     print("Доступные устройства с поддержкой WASAPI:")
#     for idx, dev in enumerate(devices):
#         if dev['hostapi'] == wasapi_api_index:
#             print(f"ID: {idx}, Name: {dev['name']}, Max Output Channels: {dev['max_output_channels']}, Max Input Channels: {dev['max_input_channels']}")
#
# if __name__ == '__main__':
#     print_wasapi_devices()


