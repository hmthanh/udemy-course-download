import requests
import os
from tqdm import tqdm
import subprocess


def download(url, path, filename):
    """
    @author Puyodead1
    """
    file_size = int(requests.head(url).headers["Content-Length"])
    if os.path.exists(path):
        first_byte = os.path.getsize(path)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(total=file_size,
                initial=first_byte,
                unit='B',
                unit_scale=True,
                desc=filename)
    res = requests.get(url, headers=header, stream=True)
    res.raise_for_status()
    with (open(path, 'ab')) as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


def download_aria(url, file_dir, filename):
    """
    @author Puyodead1
    """
    print("    > Downloading File...")
    ret_code = subprocess.Popen([
        "aria2c", url, "-o", filename, "-d", file_dir, "-j16", "-s20", "-x16",
        "-c", "--auto-file-renaming=false", "--summary-interval=0"
    ]).wait()
    print("    > File Downloaded")

    print("Return code: " + str(ret_code))
