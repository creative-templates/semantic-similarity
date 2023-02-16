import time

import pandas as pd
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
        # TODO: Handle the exception properly, SonarLint is complaining
        except:
            time.sleep(1800)
            pass

    return soups


def get_question_title(html_page: str) -> list[str]:
    titles = []

    for title_container in html_page.find_all("h3", class_="s-post-summary--content-title"):
        title = title_container.get_text()
        title = title.strip()

        if '[duplicate]' in title:
            absolute_path = get_absolute_link(title_container.find('a', _class="s-link").get('href'))
            duplicate_title = get_duplicate_question_title(absolute_path)
            print("For", title, "Duplicate title", duplicate_title.strip())
            titles.append((title, duplicate_title.strip()))

        titles.append(title)

    return titles


def get_absolute_link(relative_link: str) -> str:
    prefix = 'https;//stackoverflow.com'

    return prefix + relative_link if 'https' not in relative_link else relative_link


def get_duplicate_question_title(url: str):
    duplicate_question_page = scrap_page(url)
    aside = duplicate_question_page.find('aside')
    title = aside.find('a').get_text()

    return title.strip()


def get_all_pages_questions_title(soups: list[str]) -> list[str]:
    titles = []
    for soup in soups:
        titles.extend(get_question_title(soup))

    return titles


soups = scrap_pages(30000)
questions_title = get_all_pages_questions_title(soups)
df = pd.DataFrame(questions_title, columns=['questions'], index=None)
df = df.drop_duplicates() if df.duplicated().sum() > 0 else df
df.to_csv('questions.csv', index=False, sep=',')
