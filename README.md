# Canon camera media renamer

Rename Canon camera files with adequate names


# Prerequisites
## Problem

This is my Canon SD-card content:

- `IMG_0480.CR2`
- `IMG_0480.JPG`
- `MVI_0415.THM`
- `IMG_0479.CR2`
- `IMG_0478.CR2`
- `IMG_0479.JPG`
- `IMG_0478.JPG`
- `MVI_0477.MOV`
- `MVI_0477.THM`
- `IMG_0476.CR2`
- `MVI_0452.MOV`
- `MVI_0452.THM`
- `IMG_0476.JPG`
- `IMG_0475.CR2`
- `IMG_0475.JPG`
- `IMG_0474.CR2`
- Repeat x100...

Looks boring, right?


## Solution

Let's rename files using a following pretty format:

- `YYYYMMDD-HHMMSS-OLDNAME_1234.FMT`


### Benefits

- Not very long
- All need information in the file name
- Safely save old name


## Difficulties

There is a four formats in Canon cameras:

- `JPG` — Just a JPEG
- `CR2` — Canon Raw format
- `MOV` — QuickTime container for video files
- `THM` — Video thumbnail file

Both `JPG` and `CR2` contains EXIF data (we need it to get a shoot date).

`MOV` format knows nothing about EXIF. `THM` file will help us :-).


# Requirements

- Python 3.7
- `py3exiv2` library
