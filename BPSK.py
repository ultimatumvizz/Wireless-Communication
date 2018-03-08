# SER and BER will be same as single bit represents the symbol.

import matplotlib.pyplot as plt
import numpy as np
import random
from math import sqrt
SAMPLE_RANGE = 1000
Eb = 1
SNR_RANGE_DB = range(-10,10)

def snrLinear(SNR):
    return 10**(SNR/10.0)

def AWGNgenerate(SNR):
    N0 = Eb/float(SNR)
    MEAN = 0
    STANDARD_DEVIATION = sqrt(N0/2.0)
    return np.random.normal(MEAN,STANDARD_DEVIATION,SAMPLE_RANGE)

def randomBitsGeneration():
    BitStream = []
    for i in range(SAMPLE_RANGE):
        BitStream.append(random.randint(0,1))
    return BitStream

def genrationBPSKmodulatedBitStream(BitStream):
    modBitStream = []
    for bit in BitStream :
        if bit == 0 :
            modBitStream.append(-sqrt(Eb))
        else :
            modBitStream.append(sqrt(Eb))
    return modBitStream

def finalSignalatReceiver(modBitStream,AWGNgenerate):
    return map(lambda x,y:x+y,modBitStream,AWGNgenerate)



modRandomBits = genrationBPSKmodulatedBitStream(randomBitsGeneration())
BER = list()
for snrValue in SNR_RANGE_DB :
    receivedYStream = finalSignalatReceiver(modRandomBits,AWGNgenerate(snrLinear(snrValue)))

    errorCount = 0
    for i in range(SAMPLE_RANGE):
        if np.sign(receivedYStream[i]) != np.sign(modRandomBits[i]):
            errorCount += 1
    BER.append(errorCount/float(SAMPLE_RANGE))

print BER  

plt.semilogy(SNR_RANGE_DB, BER,'r',linewidth=2)
plt.semilogy(SNR_RANGE_DB, BER,'-s')
plt.grid(True)
plt.legend(('BER vs SNR','SER vs SNR'))
plt.xlabel('SNR (dB)')
plt.ylabel('BER')
plt.show()