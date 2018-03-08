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
    return np.random.normal(MEAN,STANDARD_DEVIATION,SAMPLE_RANGE/4)

def randomBitsGeneration():
    BitStream = []
    for i in range(SAMPLE_RANGE):
        BitStream.append(random.randint(0,1))
    return BitStream

def genration16QAMmodulatedBitStream(BitStream):
    standardMatrix = dict()
    QAMconstellation = [2,6,14,10,3,7,15,11,1,5,13,9,0,4,12,8]
    count = 0

    for i in [3,1,-1,-3]:
        for j in [-3,-1,1,3]:
            standardMatrix[QAMconstellation[count]] = complex(j,i)
            count += 1
    modBitStream = []
    for i in range(0,len(BitStream),4) :
        value = sum(map(lambda x,y:x*y,BitStream[i:i+4],[8,4,2,1]))
        modBitStream.append(sqrt(Eb/10.0)*standardMatrix[value])            
    return modBitStream

def finalSignalatReceiver(modBitStream,snrLinear):
    realPart = AWGNgenerate(snrLinear)
    imgPart  = AWGNgenerate(snrLinear)
    complexNoiseList = [complex(realPart[i],imgPart[i]) for i in range(SAMPLE_RANGE/4)]
    return [modBitStream[i] + complexNoiseList[i] for i in range(SAMPLE_RANGE/4)]


modRandomBits = genration16QAMmodulatedBitStream(randomBitsGeneration())

BER = list()
SER = list()
for snrValue in SNR_RANGE_DB :
    receivedYStream = finalSignalatReceiver(modRandomBits,snrLinear(snrValue))

    errorBER = 0
    errorSER = 0
    for i in range(0,SAMPLE_RANGE/4):
        if abs(receivedYStream[i].real - modRandomBits[i].real) >= 1 or abs(receivedYStream[i].imag - modRandomBits[i].imag) >= 1 :
            errorSER += 1 
        if abs(receivedYStream[i].real - modRandomBits[i].real) >= 1 :
            errorBER += 1
        if abs(receivedYStream[i].imag - modRandomBits[i].imag) >= 1 :
            errorBER += 1

    BER.append(errorBER/float(SAMPLE_RANGE))
    SER.append(errorSER/float(SAMPLE_RANGE/4))

print BER
print SER  

plt.semilogy(SNR_RANGE_DB,SER,'r',linewidth=2)
plt.semilogy(SNR_RANGE_DB, BER,'-s')
plt.grid(True)
plt.legend(('SER vs SNR',"BER vs SNR"))
plt.xlabel('SNR (dB)')
plt.ylabel('BER/SER')
plt.show()
