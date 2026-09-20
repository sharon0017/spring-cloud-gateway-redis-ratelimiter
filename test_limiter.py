import concurrent.futures
import requests

url = "http://localhost:8080/api/anything"

print("Firing a concurrent burst of requests...")

def send_request(req_num):
    try:
        response = requests.get(url)
        print(f"Request {req_num}: Status Code -> {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Request {req_num}: Failed -> {e}")
        return 0

# Use a thread pool to fire 30 requests at the exact same time
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(send_request, range(1, 31))