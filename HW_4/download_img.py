import argparse
from urllib.parse import urlparse
import time
import requests
import threading
from multiprocessing import Process
import asyncio
import aiohttp


def_urls_list = [
    'https://free-png.ru/wp-content/uploads/2021/07/free-png.ru-30.png',
    'https://dayonline.ru/public/article/images/2c7d53a242a05059a14677e8c0dccd788f7efa70.jpg',
    'https://w.forfun.com/fetch/4e/4e73e36e635ef13ae01d945d96369f8b.jpeg'
]

urls_list = []

class WebImage():
    def __init__(self, url, file_name):
        self.url_str = url
        self.file_name_str = file_name

    @property
    def url(self):
        return self.url_str

    @property
    def file_name(self):
        return self.file_name_str


def time_complete(func):
    def wrapper():
        time_start = time.time()
        func()
        time_end = time.time()
        print(f'Метод {func.__name__}: Изображения загружены за {time_end - time_start:.2f} секунд')

    return wrapper


def url_parse(strings):  # -> list[WebImage]:
    result = list()
    for url_str in strings:
        url = urlparse(url_str)
        file_name = url.path.split('/')[-1]
        result.append(WebImage(url_str, file_name))
    return result


def download(url, file_name):
    response = requests.get(url)#, verify=False)
    with open(file_name, 'wb') as file:
        file.write(response.content)


async def async_download(url, file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img = await response.read()
            with open(file_name, 'wb') as file:
                file.write(img)


@time_complete
def thread_method():
    threads = []
    for url in urls_list:
        thread = threading.Thread(target=download, args=[url.url, url.file_name_str])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

@time_complete
def multiprocess_method():
    processes = []
    for url in urls_list:
        process = Process(target=download, args=[url.url, url.file_name_str])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

async def async_main():
    tasks = []
    for url in urls_list:
        task = asyncio.ensure_future(async_download(url.url, url.file_name_str))
        tasks.append(task)
    await asyncio.gather(*tasks)


@time_complete
def async_code():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Загрузчик изображений по URL-адресам")
    parser.add_argument('--urls', action='extend', nargs='*',
                        help="URL изображений, указывать через пробел")
    args = parser.parse_args()
    urls_list = url_parse(def_urls_list) if not args.urls else url_parse(args.urls)

    thread_method()
    multiprocess_method()
    async_code()
