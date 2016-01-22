import argparse, sys
import csv
import numpy as np
import h5py as h5
import time


def csv_parser(step, compression, f):
    stepSlice = step
    fName = f

    with open(fName,'rb') as inputFile:
        reader = csv.reader(inputFile)

        outputFile = h5.File(fName.strip('.txt') + '_output.h5', 'w')

        print ("Converting CSV file " + f + " to HDF5 file " + outputFile.filename)

        #initialize lists to input
        headerList = []
        zoneList = []
        stepList = []

        #read in header
        reader.next()
        headerList = reader.next()
        headerCheck = len(headerList)
        headerList = headerList[2:]
        cycleCheck = len(reader.next())

        outputFile.attrs["Dataset Range"] = stepSlice
        outputFile.attrs["Dataset Naming Convention"] = "Cycle_%05d"
        outputFile.attrs["Header"] = headerList
        for i in range(len(headerList)):
            outputFile.attrs[headerList[i]] = i

        #count steps
        stepCount = 0
        outputFile.attrs["First Timestep"] = stepCount

        for row in reader:
            if row:
                #handle the header in every timestep
                if len(row) == headerCheck:
                    continue

                #timestep separator here
                if len(row) == cycleCheck:
                    #skip blank lines
                    if len(zoneList)==0:
                        continue
                    # form 3D array from zoneList, which is 2D
                    stepList.append(zoneList)
                    zoneList = []
                    stepCount += 1
                    #write to file for every "stepSlice" steps, reset array
                    if stepCount % stepSlice == 0:

                        dataArray = np.asarray(stepList, dtype='<f4')

                        #output to console & write HDF5 datasets
                        print("Writing steps " + str(stepCount - stepSlice) + "-" + str(stepCount) + " to file." )

                        write_h5(outputFile, headerList, dataArray, stepCount, stepList, compression)

                        stepList = []

                else:
                    zoneList.append(row[3:])


        write_final(outputFile, headerList, stepList, stepCount, stepSlice)
        outputFile.close()


def write_final(outputFile, headerList, stepList, stepCount, stepSlice):
    dataArray = np.asarray(stepList, dtype='<f4')

    #output to console & write HDF5 datasets
    print("Writing steps " + str(stepCount - len(stepList)) + "-" + str(stepCount) + " to file." )
    write_h5(outputFile, headerList, dataArray, stepCount, stepList)
    outputFile.attrs["Final Timestep"] = stepCount - 1


def write_h5(outputFile, headerList, dataArray, stepCount, stepList, compressed=False):
    if compressed:
        dset = outputFile.create_dataset("Cycle_%05d" % (stepCount-len(stepList)), data=dataArray, dtype='<f4', compression="gzip")
    else:
        dset = outputFile.create_dataset("Cycle_%05d" % (stepCount-len(stepList)), data=dataArray, dtype='<f4')

def main():
    cmdparser = argparse.ArgumentParser()
    cmdparser.set_defaults(compression=False)
    cmdparser.add_argument("-t","--timestep", nargs="?", default=1000, type=int, help="Enter an integer value representing the range of timesteps to slice the data into")
    cmdparser.add_argument("-f","--file", nargs="+", help="Enter any number of file names to convert to HDF5 format")
    cmdparser.add_argument("-g","--gzip", dest='compression', action='store_true', help="Enable gzip compression")
    args = cmdparser.parse_args()

    if args.file:
        for f in args.file:
            csv_parser(args.timestep, args.compression, f)
    else:
        print("Enter at least one file name")


if __name__ == "__main__":
    start = time.clock()

    main()

    end = time.clock()

def main():
    cmdparser = argparse.ArgumentParser()
    cmdparser.add_argument("-t","--timestep", nargs="?", default=1000, type=int, help="Enter an integer value representing the range of timesteps to slice the data into")
    cmdparser.add_argument("-f","--file", nargs="+", help="Enter any number of file names to convert to HDF5 format")
    args = cmdparser.parse_args()

    if args.file:
        for f in args.file:
            csv_parser(args.timestep, f)
    else:
        print("Enter at least one file name")


if __name__ == "__main__":
    start = time.clock()

    main()

    end = time.clock()
    print "Total time: %d" % (end-start)
