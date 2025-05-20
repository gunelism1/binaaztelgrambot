import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time  


BOT_TOKEN = ''
CHAT_ID = ''

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Mesaj uğurla göndərildi.")
    else:
        print("Mesaj göndərilərkən xəta:", response.text)

url = "https://bina.az/baki/alqi-satqi/menziller/yeni-tikili/4-otaqli"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

wb = Workbook()
ws = wb.active
ws.title = "Bina Siyahi"
ws.append(["Address", "Price", "Datetime", "Attributes"])

listings = soup.find_all("div", class_="items-i")

for item in listings:
    price_tag = item.find("span", class_="price-val")
    price = price_tag.get_text(strip=True) if price_tag else ""

    location_tag = item.find("div", class_="location")
    location = location_tag.get_text(strip=True) if location_tag else ""

    datetime_tag = item.find("div", class_="city_when")
    datetime = datetime_tag.get_text(strip=True) if datetime_tag else ""

    name_list = item.find("ul", class_="name")
    if name_list:
        attributes = "; ".join([li.get_text(strip=True) for li in name_list.find_all("li")])
    else:
        attributes = ""

    if price and location:
        ws.append([location, price, datetime, attributes])

        telegram_text = f"Ünvan: {location}\nQiymət: {price}\nTarix: {datetime}\nXüsusiyyətlər: {attributes}"
        send_telegram_message(telegram_text)

        time.sleep(7)  

wb.save("bina_siyahi.xlsx")
print("Uğurla yadda saxlandı: bina_siyahi.xlsx")
