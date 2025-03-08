# flipbook

Create a flipbook from a video file by extracting frames and creating tiled output layouts on a specified paper type.

The output pages can be printed and cut manually to be assembled into a flipbook.

# Setup
To install the dependencies for the script, run:

```pip install -r requirements.txt```

# Script Arguments

The script requires the following positional arguments:
* The video file to use as the source for the flipbook
* The directory in which to write the output files
* [Optional] A base name for the output files

Also there are the following options:
Frame extraction settings:
* -fr (--output-frame-rate): The frame rate at which the video frames will be extracted
* -W (--width): The width of the resulting flipbook
* -H (--height): The height of the resulting flipbook

Paper settings:
* -p (--paper-type): The paper type on which to print the flipbook frames (currently US Letter ad US Legal are options)
* -d (--dpi): The dots per inch being printed

Flipbook frame formatting settings:
* -bp (--border-padding): Padding to be applied equally to all sides of frame image
* -lp (--left-padding): Additional padding to be applied to the left side of the frame (for binding)
* -lw (--border-line-width): width of the line for the border drawn around each frame

# Running the script

Examples:

```
python create_flipbook.py input_videos/steamboat_willie_mickey.mov flipbook_output/mickey --output-frame-rate 3 --width 5 --height 3 --border-padding 30 --left-padding 180 --border-line-width 3
```
Output is the following:

```commandline
----------------------------
Input Video Info
----------------------------
Input file: input_videos/steamboat_willie_mickey.mov
Resolution: 1726.0x1298.0
Frame rate: 59.34 fps

----------------------------
Output Flipbook Format
----------------------------
Flipbook frame size: 1500x900
border_padding: 30
left_padding: 180
border_line_width: 3


Extracting frames from input_videos/steamboat_willie_mickey.mov at 3.0 FPS
 98%|█████████████████████████████████████████████████████████████████████████▊ | 441/448 [00:02<00:00, 175.54it/s]
   ...Stopping extraction at frame 441.
   ...Done extracting frames.


Saving printable flipbook to flipbook_output/mickey with paper type letter at 300 DPI.
----------------------------
Printable Flipbook Specs
----------------------------
Printed page type: US Letter
Printed page size (inches): 11.0x8.5
Printed page size (pixels): 3300x2550
Printed page dpi: 300
Frames per page: 2x2
Pages to print: 6
Output file: flipbook_output/mickey/steamboat_willie_mickey.pdf
----------------------------


Saving printable flipbook: 100%|█████████████████████████████████████████████████████| 6/6 [00:02<00:00,  2.67it/s]


Wrote flipbook_output/mickey/steamboat_willie_mickey.pdf

```


This results in a PDF with 9 pages of tiled frames, each having a watermark with the frame number.

Each page looks something like:
![](images/steamboat_willie_mickey.5.png)

The output PDF containing all tiled frames can then be printed, cut, assembled and bound into a flipbook.
