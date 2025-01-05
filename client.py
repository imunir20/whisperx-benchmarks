import requests
import time
from concurrent.futures import ThreadPoolExecutor

# URL of the server's transcribe endpoint
url = 'http://127.0.0.1:5000/transcribe'

# Path to the audio file to be sent
audio_file_path = 'hadith.m4a'

def send_request():
    with open(audio_file_path, 'rb') as f:
        files = {'audio': f}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code}")

def main():
    # Number of concurrent requests
    num_requests = 25

    print(f"Executing {num_requests} requests")
    start_time = time.time()
    print(f"Starting time: {start_time}")
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in futures:
            future.result()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Difference: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()