import requests
from bs4 import BeautifulSoup


def send(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.text


def get_cinema_from_site(cinemas, url):
    response_data = send(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    soup = soup.find_all('div', class_='cinemaList_item')
    cinemas.clear()
    exclude = [2, 3, 7, 10, 12]
    for i, m in enumerate(soup, start=1):
        if i not in exclude:
            cinemas.append(
                {
                    'id': f'{i}',
                    'name': m.findChildren('div', class_='cinemaList_name')[0].text,
                    'url': m.findChildren('a', class_='cinemaList_ref')[0].get('href')

                }
            )


def get_movie_date(movie_date, url):
    movie_date.clear()
    response_data = send(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    soup = soup.find_all('a', class_='week_day')
    for i, m in enumerate(soup, start=1):
        movie_date.append(
            {
                'id': f'{i+100}',
                'name': m.findChildren('span', class_='week_num')[0].text,
                'url': m.get('href'),


            }
        )


def get_movie_data(movie_data, url):
    movie_data.clear()
    response_data = send(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    for div in soup.find_all('div', attrs={'class': lambda x: x and 'showtimes_item showtimes_item-row' in x}):
        div.extract()
    soup = soup.find_all('div', class_='showtimes_item')

    for i, m in enumerate(soup, start=1):
        time = m.findAll('span', class_='session_time')
        price = m.findAll('span', class_='session_price')
        time_and_price_list = []
        for t in range(len(time)):
            time_and_price_list.append({
                'time': time[t].text,
                'price': price[t].text,

            })
        movie_data.append(
            {
                'id': f'{i + 200}',
                'name': m.findAllNext('span', class_='showtimesMovie_name')[0].text,
                'format': m.findAllNext('span', class_='showtimes_format')[0].text,
                'time_and_price_list': time_and_price_list,
            }
        )
