#!/usr/bin/env python3
"""
Create a JPEG with GPS lat/lon EXIF metadata only (no bearing/direction tags)
"""

from PIL import Image
import piexif

def to_rational(value):
    """Convert decimal degrees to rational (numerator, denominator) tuple"""
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = round(((value - degrees) * 60 - minutes) * 60 * 10000)
    return ((degrees, 1), (minutes, 1), (seconds, 10000))

# GPS coordinates: Tokyo, Japan  35.6762 N, 139.6503 E
lat = 35.6762
lon = 139.6503

gps_ifd = {
    piexif.GPSIFD.GPSLatitudeRef: b'N',
    piexif.GPSIFD.GPSLatitude: to_rational(lat),
    piexif.GPSIFD.GPSLongitudeRef: b'E',
    piexif.GPSIFD.GPSLongitude: to_rational(lon),
}

exif_dict = {"GPS": gps_ifd}
exif_bytes = piexif.dump(exif_dict)

img = Image.new("RGB", (200, 200), color=(100, 149, 237))
output_path = r"C:\Users\ku\Desktop\SurveyPlugin\sample\gps_latlon_only.jpg"
img.save(output_path, "JPEG", exif=exif_bytes, quality=95)

# Verify the EXIF tags
d = piexif.load(output_path)
gps = d.get('GPS', {})
tag_names = {v: k for k, v in piexif.GPSIFD.__dict__.items() if not k.startswith('_')}

print(f"Image created: {output_path}")
print("\nGPS EXIF Tags found:")
for tag_id in sorted(gps.keys()):
    value = gps[tag_id]
    tag_name = tag_names.get(tag_id, f'Tag{tag_id}')
    print(f"  {tag_name} (Tag {tag_id}): {value}")

print("\nVerification:")
print(f"  GPSLatitudeRef present: {piexif.GPSIFD.GPSLatitudeRef in gps}")
print(f"  GPSLatitude present: {piexif.GPSIFD.GPSLatitude in gps}")
print(f"  GPSLongitudeRef present: {piexif.GPSIFD.GPSLongitudeRef in gps}")
print(f"  GPSLongitude present: {piexif.GPSIFD.GPSLongitude in gps}")
print(f"  GPSImgDirection present: {piexif.GPSIFD.GPSImgDirection in gps}")
print(f"  GPSImgDirectionRef present: {piexif.GPSIFD.GPSImgDirectionRef in gps}")
