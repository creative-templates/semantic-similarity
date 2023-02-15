import time

import requests
from bs4 import BeautifulSoup


def scrap_page(link: str) -> str:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "html.parser")

    return soup


def scrap_pages(total_pages: int) -> list[str]:
    soups = []
    count = 0

    while len(soups) < total_pages:
        try:
            soup = scrap_page(f'https://stackoverflow.com/questions?tab=newest&page={count}&pagesize=50')
            soups.append(soup)
            print(f"Page {count + 1} scrapped")
            count += 1
            time.sleep(1)
        except:
            time.sleep(1800)
            pass

    return soups


def get_question_title(html_page: str) -> list[str]:
    titles = []

    for title_container in html_page.find_all("h3", class_="s-post-summary--content-title"):
        title = title_container.get_text()
        title = title.strip()
        titles.append(title)

    return titles


def get_absolute_link(relative_link: str) -> str:
    prefix = 'https;//stackoverflow.com'

    return prefix + relative_link if 'https' not in relative_link else relative_link
