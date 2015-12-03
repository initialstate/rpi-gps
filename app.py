import serial
import pynmea2
from ISStreamer.Streamer import Streamer

serialStream = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

# construct a streamer instance with information to append to or create 
# a bucket and an ini file location that contains the Initial State 
# Account Access Key.
streamer = Streamer(bucket_name="GPS Tracker", ini_file_location="./isstreamer.ini")

try:
	while True:
		sentence = serialStream.readline()
		if sentence.find('GGA') > 0:
			data = pynmea2.parse(sentence)
			streamer.log("Satellite Count", data.num_sats)
			if (data.num_sats >= 3):
				streamer.log("Location", "{lat},{lon}".format(lat=data.latitude,lon=data.longitude))
			if (data.num_sats >= 4):
				streamer.log("Altitude ({unit})".format(unit=data.altitude_units), data.altitude)
except KeyboardInterrupt:
	streamer.close()
