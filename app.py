import requests
from bs4 import BeautifulSoup
import time
import csv
import re

# Set base headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

# Brand selezionati
BRANDS = ["mg", "byd", "nio", "volkswagen", "renault", "peugeot", "skoda", "fiat", "bmw", "mercedes"]

# Helper funzione per pulire testo
def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

# --- SCRAPING CARWOW ---
def scrape_carwow():
    results = []
    base_url = "https://www.carwow.co.uk/"
    for brand in BRANDS:
        url = f"{base_url}{brand}"
        print(f"[Carwow] Scraping: {url}")
        try:
            res = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(res.content, "html.parser")
            
            # Titoli recensioni
            review_section = soup.find("div", class_="model-review__summary")
            if review_section:
                summary = clean_text(review_section.text)
            else:
                summary = "N/A"
            
            rating_tag = soup.find("div", class_="cw-score__number")
            rating = rating_tag.text.strip() if rating_tag else "N/A"

            results.append({
                "brand": brand,
                "model": "general",
                "text": summary,
                "rating": rating,
                "source": "Carwow"
            })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return results

# --- SCRAPING AUTOSCOUT24 ---
def scrape_autoscout():
    results = []
    for brand in BRANDS:
        url = f"https://www.autoscout24.com/lst/{brand}"
        print(f"[AutoScout24] Scraping: {url}")
        try:
            res = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(res.content, "html.parser")
            # Annunci auto — NO recensioni centralizzate, ma puoi estrarre descrizione annuncio
            listings = soup.find_all("div", class_="ListItem_article__ppamD")
            for listing in listings[:5]:  # Limita a 5 per esempio
                model = listing.find("h2").text if listing.find("h2") else "N/A"
                desc = listing.find("p").text if listing.find("p") else "N/A"
                results.append({
                    "brand": brand,
                    "model": model,
                    "text": clean_text(desc),
                    "rating": "N/A",
                    "source": "AutoScout24"
                })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return results

# --- SCRAPING EDMUNDS ---
# def scrape_edmunds():
#     results = []
#     for brand in BRANDS:
#         url = f"https://www.edmunds.com/{brand}/"
#         print(f"[Edmunds] Scraping: {url}")
#         try:
#             res = requests.get(url, headers=HEADERS)
#             soup = BeautifulSoup(res.content, "html.parser")
#             blocks = soup.find_all("div", class_="review-card")
#             for block in blocks[:3]:
#                 title = block.find("h3").text if block.find("h3") else "N/A"
#                 text = block.find("p").text if block.find("p") else "N/A"
#                 results.append({
#                     "brand": brand,
#                     "model": "unknown",
#                     "text": clean_text(text),
#                     "rating": "N/A",
#                     "source": "Edmunds"
#                 })
#             time.sleep(1)
#         except Exception as e:
#             print(f"Error scraping {url}: {e}")
#     return results

# --- QUATTRORUOTE --- (⚠️ limitazioni e blocchi con cookies/dynamic content)
def scrape_quattroruote():
    results = []
    base_url = "https://www.quattroruote.it/listino/"
    for brand in BRANDS:
        url = f"{base_url}{brand}.html"
        print(f"[Quattroruote] Scraping: {url}")
        try:
            res = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(res.content, "html.parser")
            # Quattroruote ha contenuti JS o bloccati — scraping limitato
            models = soup.find_all("h2")
            for m in models[:2]:
                results.append({
                    "brand": brand,
                    "model": m.text.strip(),
                    "text": "Descrizione non disponibile (JS/Paywall)",
                    "rating": "N/A",
                    "source": "Quattroruote"
                })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return results

# --- MAIN ---
def main():
    all_data = []
    all_data += scrape_carwow()
    all_data += scrape_autoscout()
    all_data += scrape_quattroruote()

    with open("recensioni_auto.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["brand", "model", "text", "rating", "source"])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"\n✅ Dataset completato con {len(all_data)} recensioni.")

if __name__ == "__main__":
    main()
