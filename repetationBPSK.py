import matplotlib.pyplot as plt
import numpy as np
import random
from math import sqrt
SAMPLE_RANGE = 10000
Eb = 1                                   # symbol energy  : a = sqrt(Eb)
SNR_RANGE_DB = range(-10,10)
repeatationLength = 4   # L == 4
def snrLinear(SNR):
    return 10**(SNR/10.0)

def AWGNgenerate(SNR,L):
    N0 = Eb/float(SNR)
    MEAN = 0
    STANDARD_DEVIATION = sqrt(N0/2.0)
    return np.random.normal(MEAN,STANDARD_DEVIATION,SAMPLE_RANGE*L)

def randomBitsGeneration():
    BitStream = []
    for i in range(SAMPLE_RANGE):
        BitStream.append(random.randint(0,1))
    return BitStream

def rayleighDistribution(L):
    # rayleigh distribution with ~CN(0,1)
    #print np.random.rayleigh(1,SAMPLE_RANGE)
    return np.random.rayleigh(1,SAMPLE_RANGE*L)

def genrationBPSKmodulatedBitStream(BitStream):
    modBitStream = []
    for bit in BitStream :
        if bit == 0 :
            modBitStream.append(-sqrt(Eb))
        else :
            modBitStream.append(sqrt(Eb))
    return modBitStream

def finalSignalatReceiverRepetationBPSK(modBitStream,snrLinear,L):
    gaussianNoise = AWGNgenerate(snrLinear,L)     # L == 4  ie repeatation length
    rayleighDistr = rayleighDistribution(L)             
    modBitStreamRepeataion = modBitStream * L
    return [ rayleighDistr[i]*modBitStreamRepeataion[i] + gaussianNoise[i] for i in range(SAMPLE_RANGE*L)]

def finalSignalatReceiverCoherentBPSK(modBitStream,snrLinear,L):
    # we need to consider only real part of "y = hx + w " as the bitstream "x" is either -1 or 1 .
    gaussianNoise = AWGNgenerate(snrLinear,L)
    rayleighDistr = rayleighDistribution(L)
    return [ rayleighDistr[i]*modBitStream[i] + gaussianNoise[i] for i in range(SAMPLE_RANGE*L)]

randomBitStream = randomBitsGeneration()
modRandomBits = genrationBPSKmodulatedBitStream(randomBitStream)

BERcoherentBPSK = list()
BERrepeatationBPSK = list()

for snrValue in SNR_RANGE_DB :
    receivedYStreamCoherentBPSK = finalSignalatReceiverCoherentBPSK(modRandomBits,snrLinear(snrValue),1)
    receivedYStreamRepeatationBPSK = finalSignalatReceiverRepetationBPSK(modRandomBits,snrLinear(snrValue),4)

    errorBERcoherentBPSK = 0 
    errorBERrepeatationBPSK = 0  

    for i in range(0,SAMPLE_RANGE):
        #### BPSK coherent
        if np.sign(receivedYStreamCoherentBPSK[i]) != np.sign(modRandomBits[i]):
            errorBERcoherentBPSK += 1

        #### BPSK repeatation 
        currentBit = modRandomBits[i]
        receivedSameRepeats = [receivedYStreamRepeatationBPSK[SAMPLE_RANGE*j+i] for j in range(4)]
        decisionValue = sum([ np.sign(value) for value in receivedSameRepeats])
        if decisionValue >= 0 and np.sign(currentBit) == -1:
            errorBERrepeatationBPSK += 1
        if decisionValue < 0 and np.sign(currentBit) == 1 :
            errorBERrepeatationBPSK += 1 

    BERcoherentBPSK.append(errorBERcoherentBPSK/float(SAMPLE_RANGE))
    BERrepeatationBPSK.append(errorBERrepeatationBPSK/float(SAMPLE_RANGE))

print BERcoherentBPSK
print BERrepeatationBPSK

plt.semilogy(SNR_RANGE_DB,BERrepeatationBPSK,'r',linewidth=2)
plt.semilogy(SNR_RANGE_DB, BERcoherentBPSK,'-s')
plt.grid(True)
plt.legend(('(BER vs SNR(BPSK repeatation)',"BER vs SNR(BPSK coherent)"))
plt.xlabel('SNR (dB)')
plt.ylabel('BERrepeationBPSK/BERcoherentBPSK')
plt.show()