"""Auto-executing module to create GPS JPEG"""
import sys
import os

def create_gps_jpeg():
    try:
        from PIL import Image
        import piexif
        
        def to_rational(value):
            degrees = int(value)
            minutes = int((value - degrees) * 60)
            seconds = round(((value - degrees) * 60 - minutes) * 60 * 10000)
            return ((degrees, 1), (minutes, 1), (seconds, 10000))
        
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
        
        d = piexif.load(output_path)
        gps = d.get('GPS', {})
        tag_names = {v: k for k, v in piexif.GPSIFD.__dict__.items() if not k.startswith('_')}
        
        output = []
        output.append(f"Image created: {output_path}")
        output.append("\nGPS EXIF Tags found:")
        for tag_id in sorted(gps.keys()):
            value = gps[tag_id]
            tag_name = tag_names.get(tag_id, f'Tag{tag_id}')
            output.append(f"  {tag_name} (Tag {tag_id}): {value}")
        
        output.append("\nVerification:")
        output.append(f"  GPSLatitudeRef present: {piexif.GPSIFD.GPSLatitudeRef in gps}")
        output.append(f"  GPSLatitude present: {piexif.GPSIFD.GPSLatitude in gps}")
        output.append(f"  GPSLongitudeRef present: {piexif.GPSIFD.GPSLongitudeRef in gps}")
        output.append(f"  GPSLongitude present: {piexif.GPSIFD.GPSLongitude in gps}")
        output.append(f"  GPSImgDirection present: {piexif.GPSIFD.GPSImgDirection in gps}")
        output.append(f"  GPSImgDirectionRef present: {piexif.GPSIFD.GPSImgDirectionRef in gps}")
        
        return True, "\n".join(output)
    except Exception as e:
        return False, f"ERROR: {e}"

if __name__ == "__main__":
    success, output = create_gps_jpeg()
    print(output)
    sys.exit(0 if success else 1)

# Auto-execute when imported
_success, _output = create_gps_jpeg()
if _success:
    print(_output)
