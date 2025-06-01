import requests
from bs4 import BeautifulSoup

def get_five_star_books(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    five_star_books = []

    books = soup.find_all('article', class_='product_pod')

    for book in books:
        rating = book.find('p', class_='star-rating')
        if rating and 'Five' in rating['class']:
            title = book.find('h3').find('a')['title']
            five_star_books.append(title)

    return five_star_books


def main():
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    all_five_star_books = []

    for page in range(1, 51):
        page_url = base_url.format(page)
        five_star_books = get_five_star_books(page_url)
        all_five_star_books.extend(five_star_books)

    with open('top_books.txt', 'w', encoding='utf-8') as f:
        for book in all_five_star_books:
            f.write(book + '\n')


if __name__ == '__main__':
    main()