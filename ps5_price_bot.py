import requests
from bs4 import BeautifulSoup
import time
import json
import os

# Telegram Setup
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot8488892376:AAHu97IqT4eNRa-zsn9c3p2HT03azxdNM6E/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Product Configuration
PRODUCTS = [
    {
        "name": "PS5 DualSense Chroma - Amazon",
        "url": "https://tinyurl.com/amazonps5indigo",
        "site": "amazon",
    },
    {
        "name": "PS5 DualSense Chroma - Flipkart",
        "url": "https://tinyurl.com/flipkartps5",
        "site": "flipkart",
    },
    {
        "name": "PS5 DualSense Chroma - Sony Store",
        "url": "https://tinyurl.com/shopatscps5",
        "site": "sony",
    },
        {
        "name": "PS5 DualSense Chroma - Croma Store",
        "url": "https://tinyurl.com/cromaps5",
        "site": "croma",
    }
]

# File to persist last prices
PRICE_FILE = "last_prices.json"

# Helpers to Save/Load Prices
def load_prices():
    if os.path.exists(PRICE_FILE):
        with open(PRICE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_prices(prices):
    with open(PRICE_FILE, "w") as f:
        json.dump(prices, f)


# Scrapers for each site
def get_amazon_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    price_str = soup.find("span", {"class": "a-price-whole"})
    if not price_str:
        return None
    return int(price_str.get_text().replace(",", "").strip())


def get_flipkart_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    price_str = soup.find("div", {"class": "_30jeq3"})
    if not price_str:
        return None
    return int(price_str.get_text().replace("₹", "").replace(",", "").strip())


def get_sony_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    price_str = soup.find("span", {"class": "product-price"})  # may need tweak
    if not price_str:
        return None
    return int(price_str.get_text().replace("₹", "").replace(",", "").strip())

def get_croma_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    # Croma usually shows price like: <span class="pdpPrice">₹5,499.00</span>
    price_str = soup.find("span", {"class": "pdpPrice"})
    if not price_str:
        return None
    return int(price_str.get_text().replace("₹", "").replace(",", "").split(".")[0].strip())

# Main Loop
def check_prices():
    last_prices = load_prices()

    for product in PRODUCTS:
        site = product["site"]
        url = product["url"]
        name = product["name"]

        try:
            if site == "amazon":
                price = get_amazon_price(url)
            elif site == "flipkart":
                price = get_flipkart_price(url)
            elif site == "sony":
                price = get_sony_price(url)
            elif site == "croma":
                price = get_croma_price(url)

            if not price:
                print(f"[{name}] Price not found.")
                continue

            old_price = last_prices.get(name)
            print(f"[{name}] Old: {old_price if old_price else 'N/A'} → New: ₹{price}")

            if old_price is None:
                last_prices[name] = price  # first run
            elif price != old_price:
                send_telegram_message(
                    f"💡 Price Update!\n{name}\nOld: ₹{old_price}\nNew: ₹{price}\n{url}"
                )
                last_prices[name] = price  # update to new price

        except Exception as e:
            print(f"Error checking {name}: {e}")

    save_prices(last_prices)


if __name__ == "__main__":
    while True:
        check_prices()
        time.sleep(3600)  # check every hour