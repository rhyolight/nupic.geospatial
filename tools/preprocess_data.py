#!/usr/bin/env python


import csv
import datetime
import sys



def preprocess(dataPath, outPath, verbose=False):
  with open(dataPath) as csvfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(open(outPath, "wb"))
    reader1 = []
    for row in reader:
      line = []
      for item in row:
        line.append(str(item))
      reader1.append(line)
    
    reader2 = reader1
    
    usedtracks = []
    for row in reader2:
      trackname = str(row[0])
      check = 0
      for track in usedtracks:
        if track == trackname:
          check += 1
      if check == 0:
        lastlat = 0
        lastlon = 0
        lasttimestamp = 0
        for i in reader1:
          keep = True
          if i[0] == trackname:
            if abs(float(i[2]) - lastlon) <= 0.0005 and abs(float(i[3]) -lastlat) <= 0.0005:
             keep = False
            if abs(int(i[1]) - lasttimestamp) <= 30:
              keep = False
            if keep == True:
              if verbose:
                print "Keeping row:\t{0}".format(row)
              writer.writerow(i)
          lastlon = float(i[2])
          lastlat = float(i[3])
          lasttimestamp = int(i[1])
        usedtracks.append(trackname)
    print len(usedtracks)
 
    

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print ("Usage: {0} "
           "/path/to/data.csv /path/to/outfile.csv").format(sys.argv[0])
    sys.exit(0)

  dataPath = sys.argv[1]
  outPath = sys.argv[2]
  preprocess(dataPath, outPath)
