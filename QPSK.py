import matplotlib.pyplot as plt
import numpy as np
import random
from math import sqrt
SAMPLE_RANGE = 1000
Eb = 1                                   # symbol energy
SNR_RANGE_DB = range(-10,10)

def snrLinear(SNR):
    return 10**(SNR/10.0)

def AWGNgenerate(SNR):
    N0 = Eb/float(SNR)
    MEAN = 0
    STANDARD_DEVIATION = sqrt(N0/2.0)
    return np.random.normal(MEAN,STANDARD_DEVIATION,SAMPLE_RANGE/2)

def randomBitsGeneration():
    BitStream = []
    for i in range(SAMPLE_RANGE):
        BitStream.append(random.randint(0,1))
    return BitStream

def genrationQPSKmodulatedBitStream(BitStream):
    modBitStream = []
    for i in range(0,len(BitStream),2) :
        if BitStream[i:i+2] == [0,0] :
            modBitStream.append(sqrt(Eb/2.0)*complex(-1,-1))
        if BitStream[i:i+2] == [0,1] :
            modBitStream.append(sqrt(Eb/2.0)*complex(-1,1))
        if BitStream[i:i+2] == [1,0] :
            modBitStream.append(sqrt(Eb/2.0)*complex(1,-1))
        if BitStream[i:i+2] == [1,1] :
            modBitStream.append(sqrt(Eb/2.0)*complex(1,1))

            
    return modBitStream

def finalSignalatReceiver(modBitStream,snrLinear):
    realPart = AWGNgenerate(snrLinear)
    imgPart  = AWGNgenerate(snrLinear)
    complexNoiseList = [complex(realPart[i],imgPart[i]) for i in range(SAMPLE_RANGE/2)]
    return [modBitStream[i] + complexNoiseList[i] for i in range(SAMPLE_RANGE/2)]



modRandomBits = genrationQPSKmodulatedBitStream(randomBitsGeneration())

BER = list()
SER = list()
for snrValue in SNR_RANGE_DB :
    receivedYStream = finalSignalatReceiver(modRandomBits,snrLinear(snrValue))

    errorBER = 0
    errorSER = 0
    for i in range(0,SAMPLE_RANGE/2):
        if np.sign(receivedYStream[i].real) != np.sign(modRandomBits[i].real) or np.sign(receivedYStream[i].imag) != np.sign(modRandomBits[i].imag):
            errorSER += 1

        if np.sign(receivedYStream[i].real) != np.sign(modRandomBits[i].real):
            errorBER += 1

        if np.sign(receivedYStream[i].imag) != np.sign(modRandomBits[i].imag) :
            errorBER += 1

    BER.append(errorBER/float(SAMPLE_RANGE))
    SER.append(errorSER/float(SAMPLE_RANGE/2))

print BER
print SER  

plt.semilogy(SNR_RANGE_DB,SER,'r',linewidth=2)
plt.semilogy(SNR_RANGE_DB, BER,'-s')
plt.grid(True)
plt.legend(('SER vs SNR',"BER vs SNR"))
plt.xlabel('SNR (dB)')
plt.ylabel('BER/SER')
plt.show()