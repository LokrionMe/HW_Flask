import requests
from multiprocessing import Process, Pool
import time
urls = ['https://w.forfun.com/fetch/b8/b8785f8630129fd3e800433b6c963b7e.jpeg',
        'https://fikiwiki.com/uploads/posts/2022-02/1644843398_53-fikiwiki-com-p-blich-krasivie-kartinki-56.jpg',
        'https://w.forfun.com/fetch/e4/e4bd5ac397e4ab52256aaf4c02ec3e35.jpeg',
        'https://klike.net/uploads/posts/2022-09/1663048876_j-25.jpg',
        'https://i.pinimg.com/originals/b1/7b/e0/b17be06871f4527711f192708284da7a.jpg',
        ]


def download(url):
    response = requests.get(url)
    filename = 'multiprocessing_' + url.rsplit('/', 1)[1]
    with open(filename, "wb") as f:
        f.write(response.content)
        print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


processes = []
start_time = time.time()
if __name__ == '__main__':
    for url in urls:
        process = Process(target=download, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f'Task completed in {time.time() - start_time:.2f}')
