from requests import Session
from bs4 import BeautifulSoup
from time import sleep
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
data = {"csrf_token": None, "username": "Dadada", "password": "Roker"}

class ThisWasLastQuotes(Exception): pass


work = Session()

work.get("https://quotes.toscrape.com/", headers=headers)

response = work.get("https://quotes.toscrape.com/login", headers=headers)

soup = BeautifulSoup(response.text, "lxml")
csrf_Token = soup.find("input").get("value")
data["csrf_token"] = csrf_Token
work.post("https://quotes.toscrape.com/login", headers=headers, data=data, allow_redirects=True)

def get_quotes():
    page = 1
    while True:
        pages = work.get(f"https://quotes.toscrape.com/page/{page}/", headers=headers)
        quotes_response = BeautifulSoup(pages.text, "lxml")
        blocks = quotes_response.find_all("div", class_="quote")

        if len(blocks) == 0:
            raise ThisWasLastQuotes("Это была последняя цытата!")

        for item in blocks:
            quote = item.find("span", class_="text").text
            author = item.find("small", class_='author').text
            yield quote, author

        page += 1


for i in get_quotes():
    print(i[0] + '\nby ' + i[1] + '\n')
    sleep(1)