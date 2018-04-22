import matplotlib.pyplot as plt
import numpy as np
import random
from math import sqrt
SAMPLE_RANGE = 100000
Eb = 1                                   # symbol energy  : a = sqrt(Eb)
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

def rayleighDistribution():
    # rayleigh distribution with ~CN(0,1)
    #print np.random.rayleigh(1,SAMPLE_RANGE)
    return np.random.rayleigh(1,SAMPLE_RANGE)

def genrationBPSKmodulatedBitStream(BitStream):
    modBitStream = []
    for bit in BitStream :
        if bit == 0 :
            modBitStream.append(-sqrt(Eb))
        else :
            modBitStream.append(sqrt(Eb))
    return modBitStream

def finalSignalatReceiverBPSK(modBitStream,AWGNgenerate):
    return map(lambda x,y:x+y,modBitStream,AWGNgenerate)

def finalSignalatReceiverCoherentBPSK(modBitStream,snrLinear,rayleighDistribution):
    # we need to consider only real part of "y = hx + w " as the bitstream "x" is either -1 or 1 .
    gaussianNoise = AWGNgenerate(snrLinear)
    
    return [ rayleighDistribution[i]*modBitStream[i] + gaussianNoise[i] for i in range(SAMPLE_RANGE)]

randomBitStream = randomBitsGeneration()
modRandomBits = genrationBPSKmodulatedBitStream(randomBitStream)

BERcoherentBPSK = list()
BERBPSK = list()
for snrValue in SNR_RANGE_DB :
    channeDistribution = rayleighDistribution()    # h[m]   ---> channel gain is based on rayleigh distribution here .
    receivedYStreamCoherentBPSK = finalSignalatReceiverCoherentBPSK(modRandomBits,snrLinear(snrValue),channeDistribution)
    receivedYStreamBPSK = finalSignalatReceiverBPSK(modRandomBits,AWGNgenerate(snrLinear(snrValue)))

    errorBERcoherentBPSK = 0 
    errorBERBPSK = 0

    for i in range(0,SAMPLE_RANGE):
        if np.sign(receivedYStreamCoherentBPSK[i]) != np.sign(modRandomBits[i]):
            errorBERcoherentBPSK += 1
        
        if np.sign(receivedYStreamBPSK[i]) != np.sign(modRandomBits[i]):
            errorBERBPSK += 1

    BERcoherentBPSK.append(errorBERcoherentBPSK/float(SAMPLE_RANGE))
    BERBPSK.append(errorBERBPSK/float(SAMPLE_RANGE))

print BERBPSK
print BERcoherentBPSK

plt.semilogy(SNR_RANGE_DB,BERBPSK,'r',linewidth=2)
plt.semilogy(SNR_RANGE_DB, BERcoherentBPSK,'-s')
plt.grid(True)
plt.legend(('(BER vs SNR(BPSK AWGN)',"BER vs SNR(BPSK coherent)"))
plt.xlabel('SNR (dB)')
plt.ylabel('BER_BPSK(BPSK)/BERcoherentBPSK')
plt.show()