import requests
import re

# Function to get Ngrok tunnel information from Ngrok API
def get_ngrok_info():
    try:
        # Ngrok API endpoint to get tunnel information
        ngrok_api_endpoint = "http://127.0.0.1:4040/api/tunnels"
        # Send GET request to Ngrok API
        response = requests.get(ngrok_api_endpoint)
        if response.status_code == 200:
            data = response.json()
            # Extracting the Ngrok URL from the first tunnel
            ngrok_url = data['tunnels'][0]['public_url']
            return ngrok_url
        else:
            print(f"Failed to get Ngrok information from Ngrok API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error getting Ngrok information: {e}")
    return None

# Function to extract Ngrok information from the URL
def extract_ngrok_info(ngrok_url):
    try:
        # Extracting the ngrok URL using regular expression
        ngrok_url_match = re.search(r"tcp://(.*):(\d+)", ngrok_url)
        if ngrok_url_match:
            ngrok_ip, ngrok_port = ngrok_url_match.group(1), ngrok_url_match.group(2)
            return ngrok_ip, ngrok_port
        else:
            print("Failed to extract Ngrok information.")
    except Exception as e:
        print(f"Error extracting Ngrok information: {e}")
    return None, None

# Function to send Ngrok information to a Discord webhook
def send_ngrok_info_to_discord(ip, port, webhook_url):
    try:
        # Prepare payload
        payload = {
            "content": f"Server is now online\n# IP: {ip}:{port}\n @here",
        }
        # Send POST request to the Discord webhook
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Ngrok information sent to Discord webhook successfully.")
        else:
            print(f"Failed to send Ngrok information to Discord webhook. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Ngrok information to Discord webhook: {e}")

# Main script
if __name__ == "__main__":
    # Get Ngrok information from Ngrok API
    ngrok_url = get_ngrok_info()

    if ngrok_url:
        print(f"Ngrok URL: {ngrok_url}")

        # Extract Ngrok information
        ngrok_ip, ngrok_port = extract_ngrok_info(ngrok_url)

        if ngrok_ip and ngrok_port:
            print(f"Ngrok IP: {ngrok_ip}, Ngrok Port: {ngrok_port}")

            # Specify your Discord webhook URL
            discord_webhook_url = "https://discord.com/api/webhooks/1199377844728496258/SJm8v3arhdQw6R49gB_oow742tqyw80inuiGra6s_g13U36xvCSrCf8wtskneftfUeAm"

            # Send Ngrok information to the Discord webhook
            send_ngrok_info_to_discord(ngrok_ip, ngrok_port, discord_webhook_url)
        else:
            print("Failed to extract Ngrok information.")
    else:
        print("Failed to get Ngrok information from Ngrok API.")
