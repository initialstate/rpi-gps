import serial
import pynmea2
import time
from ISStreamer.Streamer import Streamer

serialStream = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

# construct a streamer instance with information to append to or create 
# a bucket and an ini file location that contains the Initial State 
# Account Access Key.
streamer = Streamer(bucket_name="GPS Tracker", bucket_key="GPS_Tracker_20151126", ini_file_location="./isstreamer.ini")

try:
	while True:
		sentence = serialStream.readline()
		if sentence.find('GGA') > 0:
			data = pynmea2.parse(sentence)
			streamer.log("Location", "{lat},{lon}".format(lat=data.latitude,lon=data.longitude))
			streamer.log("Altitude ({unit})".format(unit=data.altitude_units), data.altitude)
			
			# sleep for half a second before reading again
			time.sleep(.5)
except KeyboardInterrupt:
	streamer.close()