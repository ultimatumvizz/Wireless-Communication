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

def generationOrthogonalNonCoherentBitStream(BitStream):
    modBitStream = []
    for i in range(0,len(BitStream)) :
        if BitStream[i] == 1 :
            modBitStream.append(sqrt(Eb)*complex(1,0))                      #  "1" transmitted
        else :
            modBitStream.append(sqrt(Eb)*complex(0,1))                      #  "0" transmitted            
    return modBitStream

def finalSignalatReceiver(modBitStream,snrLinear):
    realPart = AWGNgenerate(snrLinear)
    imgPart  = AWGNgenerate(snrLinear)
    rayleighRealPart = rayleighDistribution()
    rayleighImagPart = rayleighDistribution()
    complexNoiseList = [complex(realPart[i],imgPart[i]) for i in range(SAMPLE_RANGE)]
    complexRayleighDistribution = [complex(rayleighRealPart[i],rayleighImagPart[i]) for i in range(SAMPLE_RANGE)]
    return [complex(modBitStream[i].real * complexRayleighDistribution[i].real,modBitStream[i].imag * complexRayleighDistribution[i].imag) + complexNoiseList[i] for i in range(SAMPLE_RANGE)]


randomBitStream = randomBitsGeneration()
modRandomBitsBPSKaWGN = genrationBPSKmodulatedBitStream(randomBitStream)
modRandomBits = generationOrthogonalNonCoherentBitStream(randomBitStream)

BER = list()
BERBPSK = list()
for snrValue in SNR_RANGE_DB :
    receivedYStream = finalSignalatReceiver(modRandomBits,snrLinear(snrValue))
    receivedYStreamBPSK = finalSignalatReceiverBPSK(modRandomBits,AWGNgenerate(snrLinear(snrValue)))
    errorBER = 0 
    errorBERBPSK = 0
    for i in range(0,SAMPLE_RANGE):
        ########   
        N0 = Eb/float(snrLinear(snrValue))
        a = float(sqrt(Eb))
        lambdaY = ((receivedYStream[i].real**2 - receivedYStream[i].imag**2) * a**2 )/ float((a**2 + N0) * N0 )
        # if lambdaY >= 0 => "1" transmitted else 0 
        if lambdaY < 0 and modRandomBits[i] == complex(1,0):
            errorBER += 1

        if lambdaY > 0 and modRandomBits[i] == complex(0,1):
            errorBER += 1 

        if np.sign(receivedYStreamBPSK[i]) != np.sign(modRandomBitsBPSKaWGN[i]):
            errorBERBPSK += 1

    BER.append(errorBER/float(SAMPLE_RANGE))
    BERBPSK.append(errorBERBPSK/float(SAMPLE_RANGE))

print BERBPSK
print BER

plt.semilogy(SNR_RANGE_DB,BERBPSK,'r',linewidth=2)
plt.semilogy(SNR_RANGE_DB, BER,'-s')
plt.grid(True)
plt.legend(("BER vs SNR(Noncoherent orthogonal)",'BER vs SNR(BPSK AWGN)'))
plt.xlabel('SNR (dB)')
plt.ylabel('BER(BPSK)/BER(Non Coherent)')
plt.show()