# Install python 3.12 from microsoft store.
#
# pip install pillow piexif pillow_heif pyperclip
#
# [HKEY_CLASSES_ROOT\SystemFileAssociations\.heic\Shell\getlatlon]
# @="Get Lat/Lon"
# [HKEY_CLASSES_ROOT\SystemFileAssociations\.heic\Shell\getlatlon\command]
# @="C:\\scripts\\latlong.bat \"%1\""
#

from PIL import Image
from pillow_heif import register_heif_opener
import pyperclip
import sys

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif().get_ifd(0x8825)


def get_geotagging(exif):
    geo_tagging_info = {}
    if not exif:
        raise ValueError("No EXIF metadata found")
    else:
        gps_keys = ['GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
                    'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp', 'GPSSatellites', 'GPSStatus', 'GPSMeasureMode',
                    'GPSDOP', 'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack', 'GPSImgDirectionRef',
                    'GPSImgDirection', 'GPSMapDatum', 'GPSDestLatitudeRef', 'GPSDestLatitude', 'GPSDestLongitudeRef',
                    'GPSDestLongitude', 'GPSDestBearingRef', 'GPSDestBearing', 'GPSDestDistanceRef', 'GPSDestDistance',
                    'GPSProcessingMethod', 'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential']

        for k, v in exif.items():
            try:
                geo_tagging_info[gps_keys[k]] = str(v)
            except IndexError:
                pass
        return geo_tagging_info

def convert_to_degrees(value, ref):
  degrees, minutes, seconds = value.strip("()").split(',')
  decout = float(degrees) + (float(minutes) / 60) + (float(seconds) / 3600)
  if ref == 'S' or  ref == 'W':
     decout = -decout
  return "{:.5f}".format(decout)

register_heif_opener()

my_image = str(sys.argv[1])
image_info = get_exif(my_image)

results = get_geotagging(image_info)
declat = convert_to_degrees(results['GPSLatitude'], results['GPSLatitudeRef'])
declon = convert_to_degrees(results['GPSLongitude'], results['GPSLongitudeRef'])
out = str(declat) + "," + str(declon)
pyperclip.copy(out)
print(out)

with open("c:\scripts\latlon_log.txt", "a") as file:
  file.write(my_image + ',' + results['GPSAltitude'] + ',' + results['GPSImgDirection'] + ',' + out + '\r\n')



# x used to mask data
{'GPSLatitudeRef': 'N', 
'GPSLatitude': '(3x.0, 5x.0, 1x.0x)', 
'GPSLongitudeRef': 'W', 
'GPSLongitude': '(8x.0, 2x.0, 5x.2x)', 
'GPSAltitudeRef': "b'\\x00'", 
'GPSAltitude': '279.63243243243244', 
'GPSSpeedRef': 'K', 
'GPSSpeed': '0.04649941997239198', 
'GPSImgDirectionRef': 'T', 
'GPSImgDirection': '274.37165833514456', 
'GPSDestBearingRef': 'T', 
'GPSDestBearing': '27x.37165833514456', 
'GPSDateStamp': '2022:06:12'}
