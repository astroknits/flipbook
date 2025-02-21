# flipbook

Create a flipbook from a video file by extracting frames and creating tiled output layouts on a specified paper type.

The output pages can be printed and cut manually to be assembled into a flipbook.

# Setup
To install the dependencies for the script, run:

```pip install pillow opencv-python```

# Script Arguments

The script requires the following positional arguments:
* The video file to use as the source for the flipbook
* The directory in which to write the output files
* [Optional] A base name for the output files

Also there are the following options:
* -fr (--output-frame-rate): The frame rate at which the video frames will be extracted
* -p (--paper-type): The paper type on which to print the flipbook frames (currently US Letter ad US Legal are options)

# Running the script

Examples:

```
python create_flipbook.py input_videos/steamboat_willie.mov flipbook_output/mickey --frame-rate 10
```
Output is the following:

```commandline
----------------------------
Input Video Info
----------------------------
Input file: input_videos/steamboat_willie.mov
Resolution: 1726.0x1298.0
Frame rate: 59.34 fps

----------------------------
Output Formatting Info
----------------------------
ncols: 3
nrows: 3
Frame rate: 10.00 fps
Page format: US Letter
Page aspect ratio: 1.29
Frame border padding: 50
Left binding padding: 260
----------------------------


Num pages: 9
Writing output to flipbook_output/mickey/: 100%|██████████████████████████| 9/9 [00:04<00:00,  2.19it/s]


Wrote the following PDF:
flipbook_output/mickey/steamboat_willie_mickey.pdf
```


This results in a PDF with 9 pages of tiled frames, each having a watermark with the frame number.

Each page looks something like:
![](../../../Desktop/steamboat_willie_mickey.5.png)

The output PDF containing all tiled frames can then be printed, cut, assembled and bound into a flipbook.
