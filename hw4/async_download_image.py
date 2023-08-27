import asyncio
import aiohttp
import time
urls = ['https://w.forfun.com/fetch/b8/b8785f8630129fd3e800433b6c963b7e.jpeg',
        'https://fikiwiki.com/uploads/posts/2022-02/1644843398_53-fikiwiki-com-p-blich-krasivie-kartinki-56.jpg',
        'https://w.forfun.com/fetch/e4/e4bd5ac397e4ab52256aaf4c02ec3e35.jpeg',
        'https://klike.net/uploads/posts/2022-09/1663048876_j-25.jpg',
        'https://i.pinimg.com/originals/b1/7b/e0/b17be06871f4527711f192708284da7a.jpg',
        ]


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            filename = 'asyncio_' + url.rsplit('/', 1)[1]
            print(filename)
            with open(filename, "wb") as f:
                f.write(content)
                print(
                    f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
start_time = time.time()
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f'Task completed in {time.time() - start_time:.2f}')
