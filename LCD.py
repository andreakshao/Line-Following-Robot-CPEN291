import digitalio
import board
import time
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789        # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357        # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735        # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351      # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331      # pylint: disable=unused-import

#parameter is the text to write to board
def writeText(text):
    # First define some constants to allow easy resizing of shapes.
    BORDER = 5
    FONTSIZE = 16
    # Configuration for CS and DC pins (these are PiTFT defaults):
    cs_pin = digitalio.DigitalInOut(board.CE0) # setting up the cs pin
    dc_pin = digitalio.DigitalInOut(board.D25) # setting up the cd pin
    reset_pin = digitalio.DigitalInOut(board.D24) # setting up the reset pin

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 24000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()
    disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
                           cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)
    # setting up the 1.44 inch lcd
    # pylint: enable=line-too-long

    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width   # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width   # we swap height/width to rotate it to landscape!
        height = disp.height

    image = Image.new('RGB', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a green filled box as the background
    draw.rectangle((0, 0, width, height), fill=(170, 0, 136))
    disp.image(image)

#    # Draw a smaller inner purple rectangle
#    draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
#                   fill=(170, 0, 136))

    # Load a TTF Font
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', FONTSIZE)

    # Draw Some Text
    (font_width, font_height) = font.getsize(text)
    draw.text((width//2 - font_width//2, height//2 - font_height//2),
          text, font=font, fill=(255, 255, 0))

    # Display image on the LCD
    disp.image(image)

#parameter is the imageName to write to board
def writeImages(imageName):
    # Configuration for CS and DC pins (these are PiTFT defaults):
    cs_pin = digitalio.DigitalInOut(board.CE0) # setting up cs pin
    dc_pin = digitalio.DigitalInOut(board.D25) # setting up dc pin
    reset_pin = digitalio.DigitalInOut(board.D24) # setting up reset pin

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 24000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI() # setting up SPI board
    disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
                           cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)
    # creating the 1.44 inch LCD object
    # pylint: enable=line-too-long

    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width   # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width   # we swap height/width to rotate it to landscape!
        height = disp.height
    image = Image.new('RGB', (width, height))
 
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
 
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0)) # create a rectangle that is blank to put on the LCD
    disp.image(image) # put the image on the LCD
    
    image = Image.open(imageName) # open the image given by the string imageName
    
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
 
    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))
 
    # Display image.
    disp.image(image)

writeText() # call write text function
time.sleep(5) # wait 5 seconds
writeImages("blinka.jpg") # call write image on the blinka jpg file
# these three lines are to test the function