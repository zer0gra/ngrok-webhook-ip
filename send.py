import requests
import re

def get_ngrok_info():
    try:
        ngrok_api_endpoint = "http://127.0.0.1:4040/api/tunnels"
        response = requests.get(ngrok_api_endpoint)
        if response.status_code == 200:
            data = response.json()
            ngrok_url = data['tunnels'][0]['public_url']
            return ngrok_url
        else:
            print(f"Failed to get Ngrok information from Ngrok API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error getting Ngrok information: {e}")
    return None

def extract_ngrok_info(ngrok_url):
    try:
        ngrok_url_match = re.search(r"tcp://(.*):(\d+)", ngrok_url)
        if ngrok_url_match:
            ngrok_ip, ngrok_port = ngrok_url_match.group(1), ngrok_url_match.group(2)
            return ngrok_ip, ngrok_port
        else:
            print("Failed to extract Ngrok information.")
    except Exception as e:
        print(f"Error extracting Ngrok information: {e}")
    return None, None

def send_ngrok_info_to_discord(ip, port, webhook_url):
    try:
        # Prepare payload
        payload = {
            "content": f"Server is now online\n# IP: {ip}:{port}\n @here",
        }
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Ngrok information sent to Discord webhook successfully.")
        else:
            print(f"Failed to send Ngrok information to Discord webhook. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Ngrok information to Discord webhook: {e}")

# Main script
if __name__ == "__main__":
    ngrok_url = get_ngrok_info()

    if ngrok_url:
        print(f"Ngrok URL: {ngrok_url}")

        ngrok_ip, ngrok_port = extract_ngrok_info(ngrok_url)

        if ngrok_ip and ngrok_port:
            print(f"Ngrok IP: {ngrok_ip}, Ngrok Port: {ngrok_port}")

            discord_webhook_url = "your webhook here"

            send_ngrok_info_to_discord(ngrok_ip, ngrok_port, discord_webhook_url)
        else:
            print("Failed to extract Ngrok information.")
    else:
        print("Failed to get Ngrok information from Ngrok API.")
