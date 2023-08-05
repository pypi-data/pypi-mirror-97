import json
import logging

from skippy.data.decorator import consume, produce
from skippy.data.minio import download_files, upload_file


@consume()
@produce()
def handle(req, data=None):
    print("handle.(", data, ")")
    data = req + json.dumps(data)
    print("handle.(", data, ")")
    return data

def main():
    handle('bbbbbbbbbb')
    #files = download_files(urns=None)
    #upload_file(json.dumps(files),urn=None)


if __name__ == '__main__':
    main()
