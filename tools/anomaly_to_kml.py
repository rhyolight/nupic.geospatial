#!/usr/bin/env python

import csv
import xml.dom.minidom
import sys

def extractCoordinates(row):
  # This extracts the coordinates from a row and returns it as a list. This requires knowing
  # ahead of time what the columns are that hold the address information.
  return '%s,%s' % (row[2], row[3])

def createPlacemark(kmlDoc, row, order):
  # This creates a <Placemark> element for a row of data.
  # A row is a dict.
  placemarkElement = kmlDoc.createElement('Placemark')
  extElement = kmlDoc.createElement('ExtendedData')
  placemarkElement.appendChild(extElement)
  
  # Loop through the columns and create a <Data> element for every field that has a value.
  for i in range(0, len(order)):
      dataElement = kmlDoc.createElement('Data')
      dataElement.setAttribute('name', order[i])
      valueElement = kmlDoc.createElement('value')
      dataElement.appendChild(valueElement)
      valueText = kmlDoc.createTextNode(row[i])
      valueElement.appendChild(valueText)
      extElement.appendChild(dataElement)
  
  if float(row[5]) <= 0.25:
    styleElement = kmlDoc.createElement('styleUrl')
    styleElement.appendChild(kmlDoc.createTextNode('#green'))
    placemarkElement.appendChild(styleElement)
  elif float(row[5]) <= 0.75:
    styleElement = kmlDoc.createElement('styleUrl')
    styleElement.appendChild(kmlDoc.createTextNode('#yellow'))
    placemarkElement.appendChild(styleElement)
  else:
    styleElement = kmlDoc.createElement('styleUrl')
    styleElement.appendChild(kmlDoc.createTextNode('#red'))
    placemarkElement.appendChild(styleElement)
  pointElement = kmlDoc.createElement('Point')
  placemarkElement.appendChild(pointElement)
  coordinates = extractCoordinates(row)
  coorElement = kmlDoc.createElement('coordinates')
  coorElement.appendChild(kmlDoc.createTextNode(coordinates))
  pointElement.appendChild(coorElement)
  return placemarkElement


def createKML(csvReader, csvreader1, fileName, order):
  # This constructs the KML document from the CSV file.
  kmlDoc = xml.dom.minidom.Document()
  
  kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
  kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
  kmlElement = kmlDoc.appendChild(kmlElement)
  documentElement = kmlDoc.createElement('Document')
  styleElement = kmlDoc.createElement('Style')
  styleElement.setAttribute('id', 'green')
  iconstyleElement = kmlDoc.createElement('IconStyle')
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('0.5')
  scaleElement.appendChild(scaleText)
  iconstyleElement.appendChild(scaleElement)
  iconElement = kmlDoc.createElement('Icon')
  hrefElement = kmlDoc.createElement('href')
  hrefText = kmlDoc.createTextNode('http://maps.google.com/mapfiles/kml/paddle/grn-blank.png')
  hrefElement.appendChild(hrefText)
  iconElement.appendChild(hrefElement)
  iconstyleElement.appendChild(iconElement)
  styleElement.appendChild(iconstyleElement)
  documentElement.appendChild(styleElement)
  styleElement = kmlDoc.createElement('Style')
  styleElement.setAttribute('id', 'yellow')
  iconstyleElement = kmlDoc.createElement('IconStyle')
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('0.6')
  scaleElement.appendChild(scaleText)
  iconstyleElement.appendChild(scaleElement)
  iconElement = kmlDoc.createElement('Icon')
  hrefElement = kmlDoc.createElement('href')
  hrefText = kmlDoc.createTextNode('http://maps.google.com/mapfiles/kml/paddle/ylw-blank.png')
  hrefElement.appendChild(hrefText)
  iconElement.appendChild(hrefElement)
  iconstyleElement.appendChild(iconElement)
  styleElement.appendChild(iconstyleElement)
  documentElement.appendChild(styleElement)
  styleElement = kmlDoc.createElement('Style')
  styleElement.setAttribute('id', 'red')
  iconstyleElement = kmlDoc.createElement('IconStyle')
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('0.8')
  scaleElement.appendChild(scaleText)
  iconstyleElement.appendChild(scaleElement)
  iconElement = kmlDoc.createElement('Icon')
  hrefElement = kmlDoc.createElement('href')
  hrefText = kmlDoc.createTextNode('http://maps.google.com/mapfiles/kml/paddle/red-blank.png')
  hrefElement.appendChild(hrefText)
  iconElement.appendChild(hrefElement)
  iconstyleElement.appendChild(iconElement)
  styleElement.appendChild(iconstyleElement)
  documentElement.appendChild(styleElement)
  documentElement = kmlElement.appendChild(documentElement)

  # Skip the header line.
  csvReader.next()
  usedtracks = ["0"]
  for row in csvReader:
    trackName = str(row['trackName'])
    check = 0
    for track in usedtracks:
      if track == trackName:
        check += 1
    if check == 0:
        folderElement = kmlDoc.createElement('Folder')
	nameElement = kmlDoc.createElement('name')
	nameText = kmlDoc.createTextNode(trackName)
	nameElement.appendChild(nameText)
	folderElement.appendChild(nameElement)
        csvreader1.remove(csvreader1[0])
	for item in csvreader1:
	  if item[0] == trackName:	
	    placemarkElement = createPlacemark(kmlDoc, item, order)
	    folderElement.appendChild(placemarkElement)
        usedtracks.append(trackName)
	documentElement.appendChild(folderElement)

  kmlFile = open(fileName, 'w')
  kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

def anomalyrepresentation(dataPath, outPath):
  # This reader opens up 'anomaly_scores.csv'.
  # It creates a KML file called 'anomaly_representation.kml'.
  
  # If an argument was passed to the script, it splits the argument on a comma
  # and uses the resulting list to specify an order for when columns get added.
  # Otherwise, it defaults to the order used in the sample.
  
 
  order = ['trackName','timestamp','longitude','latitude','speed','anomaly_score','new_sequence']
  csvreader = csv.DictReader(open(dataPath),order)
  csvreader1 = []
  for row in csvreader:
    line = []
    for key in order:
      line.append(str(row[key]))
    csvreader1.append(line)
  csvreader = csv.DictReader(open(dataPath),order)
  kml = createKML(csvreader, csvreader1, outPath, order)

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print ("Usage: {0} "
           "/path/to/data.csv /path/to/outfile.csv").format(sys.argv[0])
    sys.exit(0)

  dataPath = sys.argv[1]
  outPath = sys.argv[2]
  anomalyrepresentation(dataPath, outPath)
