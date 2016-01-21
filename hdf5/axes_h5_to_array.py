import argparse, sys
import h5py as h5
import numpy as np
import time

#--Enable for verbose print--#
#np.set_printoptions(threshold='nan')

class Reader(object):
    
    def __init__(self, f, tStep):
        #Initiate attributes that methods can use
        self.file = h5.File(f, 'r')
        self.tStep = tStep
        self.sRange = self.file.attrs['Dataset Range']
        self.final = self.file.attrs['Final Timestep']
        self.first = self.file.attrs['First Timestep']
        
    def get_step(self, args):
        file = self.file
        tStep = self.tStep
        #Check that input is within full range of all timesteps
        if tStep < self.first or self.final < tStep:
            raise IndexError('Invalid index')
            
        # Put the index in use into the range of the correct dataset object
        index = tStep % self.sRange
        dsetNameFirst = tStep - index

        dset = file[file.attrs['Dataset Naming Convention'] % dsetNameFirst]
        
        return np.asarray(dset[index,:,:])
        
    
    
    def get_feature(self, args):
        file = self.file
        tStep = self.tStep
        feature = args.feature
        #Check that input is within full range of all timesteps
        if tStep < self.first or self.final < tStep:
            raise IndexError('Invalid index')
        
        feature = str(feature)
        if file.attrs.__contains__(feature):
            featIdx = file.attrs.__getitem__(feature)
        else:
            print ("Feature " + feature + " is not a valid feature.")
            raise AttributeError('Invalid attribute')
        
        index = tStep % self.sRange
        dsetNameFirst = tStep - index
        
        dset = file[file.attrs['Dataset Naming Convention'] % dsetNameFirst]
        
        
        if args.mode == 1:
            return np.asarray(dset[index,:,featIdx])
        else:
            return np.asarray(dset[:,:,featIdx])
        
        
    def get_zone(self, args):
        file = self.file
        tStep = self.tStep
        zone = args.zoneID
        #Check that input is within full range of all timesteps
        if tStep < self.first or self.final < tStep:
            raise IndexError('Invalid index')
        
        index = tStep % self.sRange
        dsetNameFirst = tStep - index
        
        dset = file[file.attrs['Dataset Naming Convention'] % dsetNameFirst]
        
        zoneAxisLen = dset.shape[1]
        
        if zone < 0 or zone > zoneAxisLen:
            print("You must enter a zone within the range of valid zones.")
            raise IndexError('Invalid Index')
            
        if args.mode == 1:
            return np.asarray(dset[index,zone,:])
        else:
            return np.asarray(dset[:,zone,:])
            
        
        
        
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='Enter the file name of your HDF5 file.')
    parser.add_argument('-t', '--timestep', type = int, help='Enter one integer to return array from a single timestep.')
    parser.add_argument('-m', '--mode', nargs='?', type = int, choices=[1, 2], default = 1, help='Enter a 1 for a single timestep, a 2 for all steps in Dataset.')
    subparsers = parser.add_subparsers(help='Commands')
    
    step_parser = subparsers.add_parser('step', help='Return Array from selected timestep')
    step_parser.set_defaults(method=Reader.get_step)
    
    feat_parser = subparsers.add_parser('feat', help='Return array from selected feature')
    feat_parser.add_argument('-f', '--feature', nargs ='?', type=str, help='Enter the name of a feature to return')
    feat_parser.set_defaults(method=Reader.get_feature)
    
    zone_parser = subparsers.add_parser('zone', help='Return array from selected zone')
    zone_parser.add_argument('-z', '--zoneID', nargs ='?', type=int, help='Enter an integer value representing a zone to return')
    zone_parser.set_defaults(method=Reader.get_zone)
    
    args = parser.parse_args()
 
    
    file = args.infile
    tStep = args.timestep
    
    if file:
        #print args
        runReader = Reader(file, tStep)
        dataArr = args.method(runReader, args)
        
        print dataArr
        print dataArr.shape
            

    else:
        print("Error: You did not enter a filename, program exiting.")
        sys.exit(2)
    
    
if __name__ == "__main__":
    beginClk = time.clock()
    
    main()
    
    endClk = time.clock()
    print "Total time: %02d" % (endClk-beginClk)