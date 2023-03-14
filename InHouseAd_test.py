# pip install beautifulsoup4 lxml requests
from bs4 import BeautifulSoup
import requests


# Функция преобразовывает кусок url wiki страницы в полный url
def make_url(url):
    if url and len(url) > 6 and url[:5] == '/wiki' and url[6] != "%":
        return "https://ru.wikipedia.org" + url
    return False


# Функция для парсинга страницы по url
def parse(href):
    html_text = requests.get(href).text
    soup = BeautifulSoup(html_text, 'lxml')
    links = set()
    for p in soup.find('div', class_="mw-parser-output").find_all('p'):
        for a in p.find_all('a'):
            links.add(a)
    return links


# Функция выдает готовый результат: предлжения и сами ссылки
def answer(*args):
    global start_url
    ans_path = [start_url] + list(args)
    k = 1

    for i in range(1, len(ans_path)):
        href = ans_path[i]
        parent_href = ans_path[i-1]
        html_text = requests.get(parent_href).text
        soup = BeautifulSoup(html_text, 'lxml')

        p = ''  # Текст, в котором встречается ссылка
        text = ''  # Текст ссылки

        for ipi in soup.find_all("p"):
            for ia in ipi.find_all('a'):
                if ia.get("href") == href[24:]:
                    p = ipi.text
                    text = ia.text

        # Для вывода ответа пилим предложения, добавляем точку и убираем перенос строки, где требуется
        for sent in p.split('. '):
            if text in sent:
                print(str(k)+"------------------------")
                if sent[-1] == '\n':
                    print(sent[:-1])
                else:
                    print(sent + '.')
                print(href, '\n')
                k += 1
                break


start_url = input("Введите ссылку на начальную страницу:")
finish_url = input("Введите ссылку на конечную страницу:")

# Парсим перебором, максимум 3 ссылки в глубину
# Если находим ответ, сразу выводим и заканчиваем программу
all_a1 = parse(start_url)
for a1 in all_a1:
    src1 = make_url(a1.get("href"))
    if src1:

        if src1 == finish_url:
            answer(src1)
            exit()

        all_a2 = parse(src1)
        for a2 in all_a2:
            src2 = make_url(a2.get("href"))
            if src2:

                if src2 == finish_url:
                    answer(src1, src2)
                    exit()

                all_a3 = parse(src2)
                for a3 in all_a3:
                    src3 = make_url(a3.get("href"))
                    if src3 == finish_url:
                        answer(src1, src2, src3)
                        exit()