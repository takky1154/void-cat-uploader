from aiohttp import ClientSession
import asyncio
import sys
import os
import time
loop = asyncio.get_event_loop()
tasks = []


async def upload_file(directory, file_name):
    print(f"Uploading {file_name}.....")
    async with ClientSession() as session:
        file = os.path.join(directory, file_name)
        file_size = get_human_readable_size(os.path.getsize(file))
        start_time = time.time()
        response = await session.post(f"https://upload.void.cat/src/php/upload.php?filename={file_name}", timeout=None,
        data=open(file=file, mode='rb'))
        if response.status != 200:
            print(f"Oh no: File upload failed.\nStatus code:{response.status_code}")
        else:
            elapsed_time = (time.time() - start_time) / 60
            json_resp = await response.json()
            print(f"File \"{file_name}\" uploaded: " + json_resp['link'])
            print(f"Uploaded {file_size} in {elapsed_time} minute(s).")
            await session.close()


# I thancc dah internets for this size conversion ^.^
def get_human_readable_size(size):
    for count in [' Bytes',' KB',' MB',' GB']:
        if size > -1024.0 and size < 1024.0:
            return "%3.1f%s" % (size, count)
        size /= 1024.0


if __name__ == '__main__':
    if len(sys.argv) != 2 or os.path.isdir(sys.argv[1]) != True or len(os.listdir(sys.argv[1])) < 1:
        print("You must specify a valid, non-empty folder!")
    else:
        dir = sys.argv[1]
        for file_name in os.listdir(dir):
            print(file_name)
            task = asyncio.ensure_future(upload_file(dir, file_name))
            tasks.append(task)
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
