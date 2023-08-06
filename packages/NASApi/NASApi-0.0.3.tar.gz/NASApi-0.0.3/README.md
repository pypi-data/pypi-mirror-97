# NASApi
This is a simple API wrapper for [NASA's Open APIs](https://api.nasa.gov/).

## Installation
All you need to do is install the required library.
```bash
pip install NASApi
```

In constants.py replace "DEMO_KEY" with your [NASA API key](https://api.nasa.gov/#signUp) 
```python
key = "DEMO_KEY"
```

## Usage
```python
# only import the ones you know you will use instead of importing everything
from NASApi import * 

# Simple as instantiating the class you would like to use
apods = APOD()
insights = Insight()
earths = Earth(1.5, 100.75, "2019-07-23", .15) 
epics = EPIC("enhanced", "2020-10-27")
```

## Extra Code
**Goodie #1**
Simple code for viewing the current Astronomy Picture Of the Day
```python
from NASApi import APOD
from PIL import Image

apod = APOD() # Instantiates the class
pic = Image.open(apod.bytesimage) # Opens the bytes image using PIL
pic.show() # Opens the current image for viewing pleasures 
``` 


**Goodie #2**
Simple code for viewing the images of the passed-in date and combines them into a gif for view pleasures
```python
from NASApi import EPIC
from PIL import Image

imgs = []
j = 0
epic = EPIC("enhanced", "2020-10-27") # Instantiates the class

for i in epic.images: # Goes through the images returned by the EPIC variable above
    pic = Image.open(epic.getbytesimage(i, epic.dates[j])) # Opens the current image in the list
    imgs.append(pic.convert('RGB')) # Append the current picture to the list
    j += 1 # Moves on to the next index in the list

# save_all means if True, all frames will be saved, while if False means that only the first frame will be saved
# loop means how many times the GIF should loop (0 -> infinite)
# append_image is the list of images to append as additional frames
imgs[0].save("test.gif", append_images=imgs[1:], save_all=True, loop=0, duration=300)
```
