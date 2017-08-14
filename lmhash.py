# logistic map hash library

import array
import pickle

# these limits can be as large as hardware will support
MAXHASHSIZEINBYTES = 4096
MAXNUMBEROFMAPPINGS = 1024

# this function takes a file name as input, with optional inputs for hash parameters
# it returns the hash generated from the bytes in the file, using the logistic map algorithm
# and the settings provided in the function call
def lmhash_file(inputFile, hashSizeInBytes=8, numberOfMappings=2, startingSeed=None):
  with open(inputFile, 'rb') as f:
    return lmhash_bytes(f.read(), hashSizeInBytes, numberOfMappings, startingSeed)

# this function takes a python object (string, int, class, whatever), with optional
# inputs for hash parameters; it returns the hash generated from the bytes in the object,
# using the logistic map algorithm and the settings provided in the function call
def lmhash_object(inputObject, hashSizeInBytes=8, numberOfMappings=2, startingSeed=None):
  return lmhash_bytes(pickle.dumps(inputObject), hashSizeInBytes, numberOfMappings, startingSeed)

# this function takes a bytes object, with optional inputs for hash parameters
# it returns the hash generated from the bytes using the logistic map algorithm
# and the settings provided in the function call
def lmhash_bytes(inputBytes, hashSizeInBytes=8, numberOfMappings=2, startingSeed=None):
  # check input values
  if not isinstance(inputBytes, bytes):
    raise TypeError('Attempting to call lmhash_bytes on a non-bytes object')
  if(hashSizeInBytes < 1 or hashSizeInBytes > MAXHASHSIZEINBYTES):
    raise ValueError('Hash size out of range')
  if(numberOfMappings < 1 or numberOfMappings > MAXNUMBEROFMAPPINGS):
    raise ValueError('Number of mappings out of range')
  if(startingSeed == None):
    startingSeed = bytearray([1 for x in range(hashSizeInBytes)])
  else:
    if not isinstance(startingSeed, byteArray):
      raise TypeError('Attempting to set a starting seed using a non-bytearray object')
    elif len(startingSeed) != hashSizeInBytes:
      raise ValueError('Attempting to set a starting seed with a length different from the hash length')

  # initialize temporary storage variables
  currentHashedResult = [0]*hashSizeInBytes*2
  logisticMapBuffer = [0]*(hashSizeInBytes*4 + 1)

  # apply the seed
  for i in range(hashSizeInBytes*2):
    currentHashedResult[i] = startingSeed[i% hashSizeInBytes]

  # iterate over the input
  currentPosition = 0
  inputLength = len(inputBytes)
  while(currentPosition < inputLength):
    # queue the next chunk of input
    for i in range(hashSizeInBytes):
      currentHashedResult[i] = inputBytes[(currentPosition + i) % inputLength]
    currentPosition += hashSizeInBytes

    # do the actual logistic map
    for i in range(numberOfMappings):
      # clear the buffer
      for j in range(len(logisticMapBuffer)):
        logisticMapBuffer[j] = 0

      # do x <- 960*x*(1-x)
      for j in range(hashSizeInBytes*2):
        for k in range(hashSizeInBytes*2):
          logisticMapBuffer[1 + j + k] += 960*(currentHashedResult[j])*(255 - currentHashedResult[k])

      # divide by 256 by shifting, to turn 960 into 3.75
      for j in range(hashSizeInBytes*4, 0, -1):
        logisticMapBuffer[j] = logisticMapBuffer[j-1]

      # perform carries
      for j in range(hashSizeInBytes*4, 0, -1):
        if(logisticMapBuffer[j] > 255):
          logisticMapBuffer[j-1] += logisticMapBuffer[j]//256
          logisticMapBuffer[j] = logisticMapBuffer[j] % 256

      # apply buffer to current result
      currentHashedResult = logisticMapBuffer[0:hashSizeInBytes*2]

  # return output
  return bytearray(currentHashedResult[hashSizeInBytes:hashSizeInBytes*2])

def lmhash_test():
  print('running lmhash test function ...')
  import binascii
  s1 = 'The quick brown fox jumps over the lazy dog.'
  s2 = 'The quick brown fox jumps over the lazu dog.'
  print('string 1:\t', s1, '\nhash 1:\t', binascii.hexlify(lmhash_bytes(bytes(s1, 'ascii'), hashSizeInBytes=64, numberOfMappings=10)))
  print('string 2:\t', s2, '\nhash 2:\t', binascii.hexlify(lmhash_bytes(bytes(s2, 'ascii'), hashSizeInBytes=64, numberOfMappings=10)))
  return None
