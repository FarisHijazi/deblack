# deblack

remove black frames from a video. Simple python file to create ffmpeg commands

## Usage

### rqeuirements


#### Python3

You need to have python 3 installed in the command line

#### FFmpeg

You need to have `ffmpeg` installed somehow, there are many ways to download it, one way is to download the binary (.exe) and put it in the same directory (make sure it's called ffmpeg.exe)
https://ffmpeg.org/download.html


```sh
# windows (run this in powershell)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install -y ffmpeg

# linux ubuntu
sudo apt install -y ffmpeg

# mac
brew install ffmpeg
```

### Downloading the program

```sh
pip install git+https://github.com/FarisHijazi/deblack
```

## Usage

Make sure you `cd` into the folder where both this script is and the input video.

And then just run the command:

```
deblack myvideo.mp4
```

and the output should be saved as `myvideo.out.mp4`


## History

This project originally started in as a Gist [here](https://gist.github.com/FarisHijazi/eff7a7979440faa84a63657e085ec504).

This is a combination from multiple solutions found in the bellow 2 links:
- https://video.stackexchange.com/a/16571/37220
- https://superuser.com/a/1498811/739491

helpful resources
- https://video.stackexchange.com/questions/16564/how-to-trim-out-black-frames-with-ffmpeg-on-windows#new-answer?newreg=d534934be5774bd1938b535cd76608cd
- https://github.com/kkroening/ffmpeg-python/issues/184#issuecomment-493847192


