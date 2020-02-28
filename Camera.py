from picamera import PiCamera
from time import sleep
import io
import socket
import struct
import time
import picamera
# from adafruit_st7735r import ST7735R
# import adafruit_imageload

camera = PiCamera()

stream = picamera.PiCameraCircularIO(camera, splitter_port=2)

# opens camera preview 
# unable to see if using remote access like SSH or VNC
camera.start_preview()
sleep(5)                                                # must sleep for at least 2 seconds so can sense light levels
camera.capture('/home/pi/Desktop/image.bmp', resize=(128, 128))
# displayImg()
camera.stop_preview()

def takePicture(imageName):


# make preview slightly see through so we can see errors
# camera.start_preview(alpha=200)

# Display image on the LCD
def displayImg(fileName):
    # Loads the bitmap image
    bitmap, palette = adafruit_imageload.load(fileName, bitmap=displayio.Bitmap, palette=displayio.Palette)
    # Create a TileGrid to store the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    # Create a Group to store the TileGrid
    group = displayio.Group()
    # Add the titleGrid to the Group
    group.append(tile_grid)
    # Show the group
    display.show(group)

def record():
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/testvid.h264')
    sleep(5)
    camera.stop_recording()
    camera.stop_preview()

def stream():
    camera.start_recording(stream, format='h264', splitter_port=2)
    camera.wait_recording(10, splitter_port=2)
    camera.stop_recording(splitter_port=2)

def clearStream():
    clear()


# Reference for sending stream: https://picamera.readthedocs.io/en/release-1.10/recipes1.html
# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('my_server', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg'):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # If we've been capturing for more than 30 seconds, quit
            if time.time() - start > 30:
                break
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()



