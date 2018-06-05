import string

#open files for reading and writing
gps = open('locations.log', 'r')
kml = open('plane.kml', 'w')

kml.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
kml.write('<Document>\n')
kml.write('<name>Plane Path</name>\n')
kml.write('<description>Path taken by plane</description>\n')
kml.write('<Style id=“yellowLineGreenPoly”>\n')
kml.write('<LineStyle<color>7f00ffff</color><width>4</width></LineStyle>\n')
kml.write('<PolyStyle><color>7f00ff00</color></PolyStyle>\n')
kml.write('</Style>\n')
kml.write('Placemark><name>Plane Path</name>\n')
kml.write('<styleUrl>#yellowLineGreenPoly</styleUrl>\n')
kml.write('<LineString>\n')
kml.write('<extrude>1</extrude><tesselate>1</tesselate>\n')
kml.write('<altitudeMode>relative</altitudeMode>\n')
kml.write('<coordinates>\n')

for line in gps:
    #separate string by spaces
    coordinate = string.split(line)
    longitude = coordinate[0]
    latitude = coordinate[1]
    altitude = coordinate[2]
    kml.write(longitude + "," + latitude + "," + altitude + "\n")

kml.write('<\coordinates>\n')
kml.write('</LineString>\n')
kml.write('</Placemark>\n')
kml.write('</Document>\n')
kml.write('</kml>\n')

