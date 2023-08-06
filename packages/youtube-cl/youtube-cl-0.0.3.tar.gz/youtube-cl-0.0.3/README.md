# YouTube - CL

Simple command line tool for downloading audio and video from YouTube.

**PLEASE NOTE: Requires ffmpeg to already be installed.**

## Installation
```
pip install youtube-cl
```

## Usage
### Download audio/mp3 
```bash
youtube-cl mp3 https://youtu.be/tkFOBx6j0l8
```

### Download video/mp4
```bash
youtube-cl mp4 https://youtu.be/tkFOBx6j0l8
```

### Command Line Arguments
```text
usage: youtube-cl [-h] option youtube_url

positional arguments:
  option       Option for downloading. [v] or [mp4] for video, [m] or [a] or [mp3] for audio
  youtube_url  URL of the youtube video

optional arguments:
  -h, --help   show this help message and exit
```


### Todo
- [ ] Interactive mode