import httpx
import json
import time
import random
import hashlib
import os
from colorama import *

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL

# Define the URL and headers for the request
url = "https://api-gw-tg.memefi.club/graphql"
headers = {
    "Sec-Ch-Ua": '"Chromium";v="125", "Not.A/Brand";v="24"',
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?1",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjY2NTYyMjE1ZDBiYzMwYjk4N2EzNjU2NSIsInVzZXJuYW1lIjoicXl6YW5ubiJ9LCJzZXNzaW9uSWQiOiI2NjU2MjU2MGJjNjFjZGUyMmE1ZTQyMTEiLCJzdWIiOiI2NjU2MjIxNWQwYmMzMGI5ODdhMzY1NjUiLCJpYXQiOjE3MTY5MjE2OTYsImV4cCI6MTcxNzUyNjQ5Nn0.a05lLGtYBvmQGeruHOlwcuoud9X2oDAibZK5_lbAkhs",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Mobile Safari/537.36",
    "Sec-Ch-Ua-Platform": "Android",
    "Origin": "https://tg-app.memefi.club",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://tg-app.memefi.club/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i"
}

def generate_nonce():
    return hashlib.sha256(os.urandom(32)).hexdigest()

def send_request():
    banner = f"""
    {putih}AUTO BOT {hijau}MemeFi 
    
    {putih}By: {hijau}t.me/qyzannn
    {putih}Github: {hijau}@qyzan
    
    {hijau}Message: {putih}Don't Forget To Claim Everyday !
        """
    # Generate a random tapsCount that is a multiple of 8, between desired range, e.g., 8 and 800
    taps_count = random.choice(range(8, 80, 8))
    nonce = generate_nonce()
    
    with open('payload.json', 'r') as file:
        payload = json.load(file)

    # Update the payload with the generated nonce and tapsCount
    payload = payload.copy()
    payload["variables"]["payload"]["nonce"] = nonce
    payload["variables"]["payload"]["tapsCount"] = taps_count
    
    try:
        response = httpx.post(url, headers=headers, json=payload)
        response_json = response.json()
        
        # Extract and print only the currentEnergy and coinsAmount from the response
        data = response_json.get("data", {}).get("telegramGameProcessTapsBatch", {})
        current_energy = data.get("currentEnergy")
        coins_amount = data.get("coinsAmount")

        boost = response_json.get("data", {}).get("freeBoosts", {})
        boost_coin = boost.get("currentTurboAmount")
        boost_refill = boost.get("currentRefillEnergyAmount")

        if boost_refill is not None:
            with open('boost.json', 'r') as file:
                payload_boost = json.load(file)
            
            respond = httpx.post(url, headers=headers, json=payload_boost)
            print(f'{hijau}Succes Claim Recharge')

        print("-"*80)
        print(f"{hijau}tapsCount: {putih}{taps_count}\n{hijau}nonce: {putih}{nonce}\n{hijau}currentEnergy: {putih}{current_energy}\n{hijau}coinsAmount: {putih}{coins_amount}")
        print(f"Current Turbo :{boost_coin}, Don't Forget To Claim In Your Phone!!")
        return current_energy
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        print(f"Next request in {mins:02d}:{secs:02d} ", flush=True, end="\r")
        time.sleep(1)
        seconds -= 1


# Send the request repeatedly
while True:
    current_energy = send_request()
    if current_energy <= 100:
        print("-"*80)
        print(f"{merah}Current energy is 100, sleeping for 16 minutes.")
        countdown_timer(960)  # Sleep for 30 minutes
    else:
        countdown_timer(1)  # Adjust the sleep duration as needed for regular requests
        random_time = random.randint(1,5)
        countdown_timer(random_time)
    # If there was an error and current_energy is None, wait a short period before retrying
    
