import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
# URL of the server's transcribe endpoint
url = 'http://127.0.0.1:5000/transcribe'

# Path to the audio file to be sent
audio_file_path = 'hadith.m4a'

def send_request():
    with open(audio_file_path, 'rb') as f:
        files = {'audio': f}
        start = time.time()
        response = requests.post(url, files=files)
        duration = time.time() - start
        if response.status_code == 200:
            print(f"Request completed in {duration:.2f}s")
            return duration
        else:
            print(f"Error: {response.status_code}, Duration: {duration:.2f}s")
            return None

def main():
    import psutil
    import os
    process = psutil.Process(os.getpid())

    for power in range(6):  # 2^5 = 32 max concurrent requests
        num_requests = 2 ** power
        print(f"\n=== Testing with {num_requests} concurrent requests ===")
        
        start_time = time.time()
        durations = []
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(send_request) for _ in range(num_requests)]
            for future in as_completed(futures):
                if result := future.result():
                    durations.append(result)
        
        total_time = time.time() - start_time
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        cpu_percent = process.cpu_percent()
        
        if durations:
            avg_duration = sum(durations) / len(durations)
            print(f"\nResults for {num_requests} requests:")
            print(f"Total time: {total_time:.2f}s")
            print(f"Average response time: {avg_duration:.2f}s")
            print(f"Min response time: {min(durations):.2f}s")
            print(f"Max response time: {max(durations):.2f}s")
            print(f"\nResource Usage:")
            print(f"CPU Usage: {cpu_percent:.1f}%")
            print(f"Memory Usage: {final_memory:.1f}MB (Change: {final_memory - initial_memory:+.1f}MB)")
            print(f"Threads: {len(process.threads())}")
        
        # Optional: Add delay between batches to let server recover
        time.sleep(2)
if __name__ == '__main__':
    main()