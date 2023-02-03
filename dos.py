import requests

url = "http://92.92.218.147:42100"
image_path = "static/upload.svg"

with open(image_path, "rb") as image:
    files = {"file": image}
    for i in range(60):
        response = requests.post(url, files=files)
        print(response.status_code)

