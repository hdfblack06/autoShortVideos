# Auto Short Videos

Making Short Videos Using Python
[![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen)](https://github.com/hdfblack06/autoShortVideos/)

## Install Requirements

| required     | Download                                                             |
| ------------ | -------------------------------------------------------------------- |
| ffmpeg       | [Download FFMPEG](https://ffmpeg.org/)                               |
| Image Magick | [Download Image Magick](https://imagemagick.org/script/download.php) |

> Note: `ffmpeg.exe And ffplay.exe And ffprobe.exe` Are Required And Should Be Located In The Same Directory As `autoShortVideos.py`.

> Note: Create `.env` File Put Path Of Image Magick
> E.g.: `IMAGEMAGICK_BINARY="C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"`

## Install Requirements

```sh
pip install -r requirements.txt
```

## Donwload Videos

> Video Should Be `1440p` and `.webm`
> You Can Have Multi Videos
> Put Your Videos Inside `BackGroundVideos` Folder

## Stories

> Sroties Should Be Named `Story_[Index].txt` And Should Be Inside Folder Named `Stories`
> You Can Have Multi `Story_[Index].txt` Stories With Different Index `Story_1.txt, Story_2.txt ...`

## Executing Script

```sh
python .\autoShortVideos.py
```

## Version History

- `1.0.0`
  Initial Release

# Enjoy

[![GitHub Profile](https://img.shields.io/badge/GitHub-hdfblack06-blue)](https://github.com/hdfblack06)
