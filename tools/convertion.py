import csv
import time
import calendar

def readais(dataPath):
	"""It opens the original file, takes all the information and stores it in filelist. Then return file list"""

	my_file = open(dataPath,'rb')
	reader = csv.reader(my_file)
	filelist = []
	for row in reader:
		rowlist = []
		for item in row:
			rowlist.append(item)
		filelist.append(rowlist)
		rowlist = []
	my_file.close()
	return filelist

def aisconvertion(filelist):
	"""It takes filelist and changes it to the format required by nupic.geospatial"""
	fileconverted = []
	for i in range(1,int(len(filelist))):
		rowlist = []
		rowlist.append(filelist[i][0])
		timetuple = time.strptime(str(filelist[i][6]),"%Y-%m-%dT%H:%M:%S")
		dt = calendar.timegm(timetuple)
		rowlist.append(int(dt))
		rowlist.append(filelist[i][2])
		rowlist.append(filelist[i][1])
		rowlist.append("")
		speed = float(filelist[i][3]) * 0.05144
		rowlist.append(speed)
		rowlist.append("")
		rowlist.append(1)

		fileconverted.append(rowlist)

		rowlist = []

	return fileconverted

def writeais(outPath,fileconverted):
	"""Writes the converted file returned by convertion in the file that we will run with nupic.geospatial"""

	my_file = open(outPath,'wb')
	writer = csv.writer(my_file, delimiter=',', quotechar="", quoting=csv.QUOTE_NONE)
	for row in fileconverted:
		writer.writerow(row)
	my_file.close()

def convertion(dataPath, outPath):

  filelist = readais(dataPath)
  fileconverted = aisconvertion(filelist)
  writeais(outPath, fileconverted)


if __name__ == "__main__":
  if len(sys.argv) < 3:
    print ("Usage: {0} "
           "/path/to/data.csv /path/to/outfile.csv").format(sys.argv[0])
    sys.exit(0)

  dataPath = sys.argv[1]
  outPath = sys.argv[2]
  convertion(dataPath, outPath)
