import requests
from uuid import uuid4

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
        # Start the download
        self.length = requests.get(self.url, stream=True).headers["Content-length"]
        self.length = int(self.length)
        
        self.chunks = []
        for i in range(1,THREADS):
            chunksize = self.length
            chunk = {
                "filename": uuid4(),
                "bytes": (chunksize*(i-1),chunksize*i)
            }
            self.chunks.append(chunk)
            self.start_chunk(self.url)
        pass
    
    def start_chunk(self, url, chunk):
        
        pass