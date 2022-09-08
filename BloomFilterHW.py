from BitHash import BitHash
from BitVector import BitVector
import cityhash

class BloomFilter(object):
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        # compute the estimated proportion og bits still zero 
        phi = 1 - ((maxFalsePositive) ** (1 / numHashes)) 
        
        # use phi computed in previous step to compute the number of bits needed
        N = int(numHashes / (1 - (phi ** (1 / numKeys))))
        
        return N    
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.   
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        self.__n = numKeys 
        self.__d = numHashes 
        self.__p = maxFalsePositive
        self.__N = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__bloomFilter = BitVector(size = self.__N)
        self.__setBits = 0
      
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works   
    def insert(self, key):
        
        # for each time the client wants to hash the key 
        for i in range(self.__d):
            
            # find the hash value of the key in this bloom filter 
            hashVal = BitHash(key, i+1) % self.__N
        
            # check that the bit has not already been set in the bloom filter
            if self.__bloomFilter[hashVal] != 1: 
                
                # set the bit at location of the hash value in the bloom filter
                self.__bloomFilter[hashVal] = 1
                
                # increment the number of set bits
                self.__setBits += 1

    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        
        # for each time the client wants to hash the key         
        for i in range(self.__d):
            
            # find the hash value of the key in this bloom filter             
            hashVal = BitHash(key, i+1) % self.__N
            
            # if there is a zero at any of the bit locations of the hash value
            # immedediately return False, otherwise return true
            if self.__bloomFilter[hashVal] == 0:
                return False
        
        # at this point, never encountered a zero so return True
        return True 
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero.    
    def falsePositiveRate(self):
        
        # find the actual proportion of bits that are still zero
        realPhi = (1 - (self.__d / self.__N)) ** self.__n
        
        # compute the current projected false positive rate 
        projCurrP = (1 - realPhi) ** self.__d 
        
        return projCurrP
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.  
    def numBitsSet(self):
        return self.__setBits

    # method for len to use in main 
    def __len__(self):
        return self.__N

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    bF = BloomFilter(numKeys, numHashes, maxFalse)
    
    # open the text file and read the first line
    fin = open("wordlist.txt")
    line = fin.readline()
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    for i in range(numKeys):
        bF.insert(line)
        line = fin.readline()
    
    fin.close()
    
    print(bF.falsePositiveRate() * 100)
    
    # re-open the file and set line to be the first line of the text file 
    fin = open("wordlist.txt")
    line = fin.readline()
    
    # initiate count to count how many are not found
    countMissing = 0
    
    # loop through the inserted keys and if the line is not found, increment count 
    for i in range(numKeys):
        if not bF.find(line): countMissing += 1
        line = fin.readline()
        
    print(countMissing)
    
    
    # starting from the line the find loop finished at (so the next lines were not
    # inserted) and check if they can be found in the bF - if they can be found
    # it is a false positive 
    
    # initialize false count to count how many are falsely found 
    countFalseFound = 0 
    
    # loop through the non inserted keys and if they are found increment count 
    for i in range(numKeys):
        if bF.find(line): countFalseFound += 1
        line = fin.readline()
    
    fin.close()
    print(countFalseFound)    

    # calculate the actual false positive rate based on what was inserted and found
    actualFalsePosRate = (countFalseFound / numKeys) * 100
    print(actualFalsePosRate)
    
if __name__ == '__main__':
    __main()       

