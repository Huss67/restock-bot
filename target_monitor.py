import time
import requests
from bs4 import BeautifulSoup

# 👉 Discord webhook (replace this)
DISCORD_WEBHOOK = "YOUR_DISCORD_WEBHOOK_HERE"

CHECK_INTERVAL = 20

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -----------------------
# PRODUCTS (NOW 4 ITEMS)
# -----------------------
PRODUCTS = [
    {
        "name": "Pokémon Mega Gardevoir",
        "url": "https://www.target.com/p/pok-233-mon-trading-card-game-mega-evolution-ascended-heroes-premium-poster-collection-mega-gardevoir/-/A-95093982"
    },
    {
        "name": "Ascended Heroes Booster Bundle",
        "url": "https://www.target.com/p/tempo/-/A-95120834?clkid=101028f1Nc15911f081dc03936f784b46&cpng=&TCID=AFL-101028f1Nc15911f081dc03936f784b46&afsrc=1&lnm=81938&afid=Tempom&ref=tgt_adv_xasd0002"
    },
    {
        "name": "Pokemon Lucario EX Box",
        "url": "https://www.target.com/p/pokemon-tcg-mega-evolution-ascended-heroes-premium-poster-collection-mega-lucario/-/A-1010583462#lnk=sametab"
    },
    {
        "name": "Ascended Heroes ETB",
        "url": "https://www.target.com/p/2025-pok-me-2-5-elite-trainer-box/-/A-95082118?nrtv_cid=epvyknijmd8id&clkid=d6cbae30N2cc811f19d2b05cc80f71658&cpng=PTID3&TCID=AFL-d6cbae30N2cc811f19d2b05cc80f71658&afsrc=1&lnm=201333&afid=Howl%20Technologies%2C%20Inc.&ref=tgt_adv_xasd0002"
    }
]

# tracks previous stock state to avoid spam alerts
state = {}

def send_discord(name, url):
    data = {
        "content": f"🔥 **IN STOCK ALERT** 🔥\n{name}\n{url}"
    }
    requests.post(DISCORD_WEBHOOK, json=data)


# =========================
# 🔥 IMPROVED STOCK CHECKER
# =========================
def check_stock(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        text = r.text.lower()

        # ❌ strong negative signals (always trust these first)
        if "out of stock" in text or "sold out" in text:
            return False

        # ⚠️ Target often still shows "add to cart" even when fake
        has_cart = "add to cart" in text
        has_ship = "ship it" in text or "deliver it" in text

        # EXTRA SAFETY CHECK:
        # real stock pages usually also include price container
        has_price = "$" in text

        # final decision (more strict = fewer false positives)
        if has_cart and has_ship and has_price:
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False


print("🚀 Multi-product monitor started...")

while True:
    for product in PRODUCTS:
        name = product["name"]
        url = product["url"]

        in_stock = check_stock(url)

        # initialize state
        if name not in state:
            state[name] = False

        # alert only on OUT → IN transition
        if in_stock and not state[name]:
            print(f"🔥 IN STOCK: {name}")
            send_discord(name, url)
            state[name] = True

        elif not in_stock:
            print(f"❌ Out of stock: {name}")
            state[name] = False

    time.sleep(CHECK_INTERVAL)