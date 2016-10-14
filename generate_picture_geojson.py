"""
Find positions according to nas-track and picture capture date.
"""
import json
import datetime
import exifread
import netCDF4
import numpy as np

def creation_date(path):
    with open(path, 'rb') as filehandle:
        tags = exifread.process_file(filehandle, stop_tag="EXIF DateTimeOriginal")
    date = tags["EXIF DateTimeOriginal"]
    return datetime.datetime.strptime(date.values, '%Y:%m:%d %H:%M:%S')

class TimeLocator(object):
    def __init__(self, nasdata):
        self._time = nasdata.variables["TIME"][:]
        self._time_unit = nasdata.variables["TIME"].units
        self._lat = nasdata.variables["IRS_LAT"][:]
        self._lon = nasdata.variables["IRS_LON"][:]
    def get_position(self, date):
        date = netCDF4.date2num(date, self._time_unit)
        return np.interp(date, self._time, self._lat), np.interp(date, self._time, self._lon)


def _main():
    import sys
    nasfile = sys.argv[1]
    pictures = sys.argv[2:]
    locator = TimeLocator(netCDF4.Dataset(nasfile))
    points = []
    for picture in pictures:
        time = creation_date(picture)
        lat, lon = locator.get_position(time)
        points.append({"type": "Feature",
                       "geometry": {
                            "type": "Point",
                            "coordinates": [lon, lat]
                        },
                       "properties": {
                            "type": "picture",
                            "creation_date": time.isoformat(),
                            "path": picture
                        }
                       })
    out = {"type": "FeatureCollection", "features": points}
    print json.dumps(out)


if __name__ == '__main__':
    _main()
