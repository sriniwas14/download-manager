import requests
from uuid import uuid4
import time

THREADS = 6
class Download:
    def __init__(self, url) -> None:
        self.url = url
        self.start()
        pass

    def pause(self) -> None:
        # Pause the current download
        pass

    def start(self) -> None:
        self.started_at = time.time()
        # Start the download
        data_request = requests.get(self.url, stream=True)
        # Checking if the server supports range requests.
        self.range = data_request.headers.get("Accept-Ranges")
        # The above code is converting the length of the data request into an integer.
        self.length = int(data_request.headers["Content-length"])

        if self.range != "bytes":
            return self.single_thread_download()  # start direct download

        # Creating a list of chunks that will be downloaded.
        self.chunks = []
        for i in range(1, THREADS):
            chunksize = self.length//THREADS-1
            chunk = {"filename": uuid4(), "bytes": (chunksize * (i - 1), chunksize * i)}
            self.chunks.append(chunk)
            self.start_chunk(self.url, chunk)
        print("File Downloaded! in ", time.time()-self.started_at)
        pass

    def single_thread_download(self):
        local_filename = self.url.split("/")[-1]
        file_req = requests.get(self.url, stream=True)
        with file_req as r:
            self.save_file(local_filename, r)
        pass

    def save_file(self, filename, read_stream):
        with open(filename, "wb") as f:
            for chunk in read_stream.iter_content(chunk_size=8192):
                f.write(chunk)
        pass

    def start_chunk(self, url, chunk):
        bytes = chunk["bytes"]
        filename = chunk["filename"]
        print("BTS ", self.length, bytes, filename)
        file_req = requests.get(url, headers={"Range": f"bytes={bytes[0]}-{bytes[1]}"})
        with file_req as r:
            self.save_file(f"./Downloads/{filename}", r)
        pass
