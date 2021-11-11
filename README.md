# Udemy course downloader

- Download Udemy course Enrolled and Udemy enterprise
https://pythonrepo.com/repo/Puyodead1-udemy-downloader-python-downloader

## Requirements

* Install pip package

```sh
pip install -r requirements.txt
```

* `ffmpeg`, `aria2c`, `mp4decrypt` (from Bento4 SDK) and ``yt-dlp`` (``pip install yt-dlp``).
Add bin to PATH windows (only support for Windows)

* Chrome Extention:

  * `widevine-l3-guesser` : https://github.com/Satsuoni/widevine-l3-guesser.git
  Download and install Developer mode for Chrome extention

## Usage

### Prepare:

* bearer_token : in Chrome open Inspect Element or Developer Tools, go to Network Tab, search `api-2.0`

* Step 1 : Edit args.bearer_token variable in main.py file
* Step 2 : Get 

Load widevine-l3-guesser chrome extention by Developer Mode -> Go to udemy course site -> Open Chrome terminal (inspect element) -> KeyID and Key appear on log

- KeyID : ex. 9a7e6613f573435781703182c07fc89
- Key : ex. e2428b2d3751fd2692d1a40ea3c1d71
(Using widevine-l3-guesser to get)
