# Udemy course downloader

- Download Udemy course Enrolled and Udemy enterprise

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

Parameter require and sample

#### .env file:

- UDEMY_BEARER=0dVcR5LCz0YsjL8sG6kYHSxjjkR0bvwGdxWlrJ2Jh
- UDEMY_COURSE_ID=947098

#### keyfile.json

Load widevine-l3-guesser chrome extention by Developer Mode -> Go to udemy course site -> Open Chrome terminal (inspect element) -> KeyID and Key appear on log

- KeyID : ex. 9a7e6613f573435781703182c07fc89
- Key : ex. e2428b2d3751fd2692d1a40ea3c1d71
(Using widevine-l3-guesser to get)


## Advanced Usage

```
usage: main.py [-h] -c COURSE_URL [-b BEARER_TOKEN] [-q QUALITY] [-l LANG] [-cd CONCURRENT_DOWNLOADS] [--skip-lectures] [--download-assets]
               [--download-captions] [--keep-vtt] [--skip-hls] [--info]

Udemy Downloader

optional arguments:
  -h, --help            show this help message and exit
  -c COURSE_URL, --course-url COURSE_URL
                        The URL of the course to download
  -b BEARER_TOKEN, --bearer BEARER_TOKEN
                        The Bearer token to use
  -q QUALITY, --quality QUALITY
                        Download specific video quality. If the requested quality isn't available, the closest quality will be used. If not
                        specified, the best quality will be downloaded for each lecture
  -l LANG, --lang LANG  The language to download for captions, specify 'all' to download all captions (Default is 'en')
  -cd CONCURRENT_DOWNLOADS, --concurrent-downloads CONCURRENT_DOWNLOADS
                        The number of maximum concurrent downloads for segments (HLS and DASH, must be a number 1-50)
  --skip-lectures       If specified, lectures won't be downloaded
  --download-assets     If specified, lecture assets will be downloaded
  --download-captions   If specified, captions will be downloaded
  --keep-vtt            If specified, .vtt files won't be removed
  --skip-hls            If specified, hls streams will be skipped (faster fetching) (hls streams usually contain 1080p quality for non-drm
                        lectures)
  --info                If specified, only course information will be printed, nothing will be downloaded
```

- Passing a Bearer Token and Course ID as an argument
  - `python main.py -c <Course URL> -b <Bearer Token>`
  - `python main.py -c https://www.udemy.com/courses/myawesomecourse -b <Bearer Token>`
- Download a specific quality
  - `python main.py -c <Course URL> -q 720`
- Download assets along with lectures
  - `python main.py -c <Course URL> --download-assets`
- Download assets and specify a quality
  - `python main.py -c <Course URL> -q 360 --download-assets`
- Download captions (Defaults to English)
  - `python main.py -c <Course URL> --download-captions`
- Download captions with specific language
  - `python main.py -c <Course URL> --download-captions -l en` - English subtitles
  - `python main.py -c <Course URL> --download-captions -l es` - Spanish subtitles
  - `python main.py -c <Course URL> --download-captions -l it` - Italian subtitles
  - `python main.py -c <Course URL> --download-captions -l pl` - Polish Subtitles
  - `python main.py -c <Course URL> --download-captions -l all` - Downloads all subtitles
  - etc
- Skip downloading lecture videos
  - `python main.py -c <Course URL> --skip-lectures --download-captions` - Downloads only captions
  - `python main.py -c <Course URL> --skip-lectures --download-assets` - Downloads only assets
- Keep .VTT caption files:
  - `python main.py -c <Course URL> --download-captions --keep-vtt`
- Skip parsing HLS Streams (HLS streams usually contain 1080p quality for Non-DRM lectures):
  - `python main.py -c <Course URL> --skip-hls`
- Print course information only:
  - `python main.py -c <Course URL> --info`
- Specify max number of concurrent downloads:
  - `python main.py -c <Course URL> --concurrent-downloads 20`
  - `python main.py -c <Course URL> -cd 20`