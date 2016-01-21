import argparse, sys
import h5py as h5
import numpy as np
import time


class Reader(object):
    
    def __init__(self, f):
        #Initiate attributes that methods can use
        self.file = h5.File(f, 'r')
        self.sRange = self.file.attrs['Dataset Range']
        self.final = self.file.attrs['Final Timestep']
        self.first = self.file.attrs['First Timestep']
        
    def get_step(self, tStep):
        #Check that input is within full range of all timesteps
        if tStep < self.first or self.final < tStep:
            raise IndexError('Invalid index')
            
        # Put the index in use into the range of the correct dataset object
        index = tStep % self.sRange
        dsetNameFirst = tStep - index

        dset = self.file[self.file.attrs['Dataset Naming Convention'] % dsetNameFirst]
        
        return np.asarray(dset[index,:,:], dtype='f4')
    
    #This method currently uncalled, as the Reader.get_block method is more efficient. 
    def get_mult_step(self, start, stop): 
        # Check for range error first, to prevent iteration in error case
        if start < self.first or self.final < stop or stop < start:
            raise IndexError('Invalid index')
        
        dList = range(start, stop + 1)
        
        #Loop over input range, bring in a temporary 2D array, and reshape it into a list of 2D arrays
        for i in range(len(dList)):
            tArr = self.get_step(i + start)
            tShape = tArr.shape 
            dList[i] = np.reshape(tArr, (1, tShape[0], tShape[1]))
        
        #Concatenate list of 2D arrays vertically for 3D array
        dArr = np.concatenate(dList, axis=0)
        return dArr
        
    def get_block(self, start, stop):
        # Check for range error first, to prevent iteration in error case
        if start < self.first or self.final < stop or stop < start:
            raise IndexError('Invalid index')
            
        step = start
        
        while step < stop:
            # Set the start and stop points within the dataset
            thisFirst = step % self.sRange
            thisRange = self.sRange
            
            # Record the timestep number for use in grabbing dataset name
            dsetNameFirst = step - thisFirst
            
            #Handle the indexing when the reader crosses the boundary of one dataset to the next
            if dsetNameFirst + thisRange > stop:
                thisRange = stop - dsetNameFirst + 1
            
            #Use h5 attribute to open dataset name, write array from user input
            dset = self.file[self.file.attrs['Dataset Naming Convention'] % dsetNameFirst]
            dArr = np.asarray(dset[thisFirst:thisRange,:,:], dtype='f4')
            
            #If first step, create array. Else any subsequent step, concatenate on the vertical axis to make array 3D
            if start == step:
                dList = dArr
            else:
                dList = np.concatenate((dList, dArr), axis=0)
            
            # Add dataset range for iteration
            step = dsetNameFirst + thisRange
            
        return dList
        
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Enter the file name of your HDF5 file.')
    parser.add_argument('-t', '--timestep', nargs='+', type = int, help='Enter one integer to return array from single timestep, two to return a range of timesteps.')
    parser.add_argument('-s', '--switch', nargs='?', default = 0, type = int, help='Enter a 0 to use the faster block read method, or a 1 to use slower mult_step method for testing. Defaults to 0.')
    args = parser.parse_args()
    
    file = args.file
    tStep = args.timestep
    switch = args.switch
    
    if file:
            runReader = Reader(file)
            
            #Read from single timestep if one arg
            if len(tStep) == 1:
                tStep = int(tStep[0])
                
                try:
                    dataArr = runReader.get_step(tStep)
                except:
                    print("Error single: Value outside the range of timesteps, program exiting.")
                    sys.exit(2)
                
            #Read from range of timesteps if two args
            elif len(tStep) == 2:
                start = int(tStep[0])
                stop = int(tStep[1])

                try:
                    if switch == 0:
                        dataArr = runReader.get_block(start, stop)
                    elif switch == 1:
                        dataArr = runReader.get_mult_step(start, stop)
                    else:
                        print ("Error: Value of switch must be 0 or 1")
                        raise IndexError('Invalid Index')
                except:
                    print("Error multi: Value outside the range of timesteps or allowed parameters, program exiting.")
                    sys.exit(2)

            #Check for too many args
            else:
                print("Error: Too many timestep arguments, program exiting.")
                sys.exit(2)
            
            print( "Shape of array: " + str(dataArr.shape))
            
    #Error check for lack of file
    else:
        print("Error: You did not enter a filename, program exiting.")
        sys.exit(2)
    
    
if __name__ == "__main__":
    beginClk = time.clock()
    
    main()
    
    endClk = time.clock()
    print "Total time: %02d" % (endClk-beginClk)