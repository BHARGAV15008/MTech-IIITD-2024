from collections import Counter
import os
import time
import hashlib
from matplotlib.widgets import Lasso
import numpy as np
import random as rnd
from PIL import Image
from scipy.fft import fft
from scipy.fftpack import dct
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import get_window
from scipy.ndimage import gaussian_filter
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# File Paths:
imgPath = './Semester 1/Machine Learning/Assignment/Datasets/MLA2_DATA/IMAGE'
imgFiles = os.listdir('./Semester 1/Machine Learning/Assignment/Datasets/MLA2_DATA/IMAGE')
print(imgFiles)

audPath = './Semester 1/Machine Learning/Assignment/Datasets/MLA2_DATA/AUDIO'
audioFiles = os.listdir(audPath)

# Random Number Generator
def genRandom(seed=None, noBytes=None, fromVal=0, toVal=799):
    time.sleep(0.5)
    if seed == None:
        seed = int(time.time_ns())
    
    state = seed.to_bytes(32, 'big')
    def _sha256(data):
        return hashlib.sha256(data).digest()

    if noBytes is not None:
        result = b''
        while len(result) < noBytes:
            state = _sha256(state)
            result += state
        return int.from_bytes(result[:noBytes], 'big')  # Convert bytes to integer

    if fromVal is not None and toVal is not None:
        rand_bytes = genRandom(seed, 4)  # Generate 4 random bytes
        rand_int = rand_bytes % (toVal - fromVal + 1) + fromVal
        return rand_int


# Function to plot images
def plotImages(axis, img, title, fontSize=12, cmap=None):
    axis.imshow(img, cmap=cmap)
    axis.set_title(title, fontsize=fontSize)
    axis.axis('off')

# Function for Min-Max Normalization without numpy array
def minMaxNormalizationNA(actualData):
    minD = min(actualData)
    maxD = max(actualData)
    normalizedData = [
        int(255 * (value - minD) / (maxD - minD)) if maxD > minD else 0
        for value in actualData
    ]
    return normalizedData 

# Normalization Function with numpy array
def minMaxNormalization(actualData, xtoy):
    x, y = xtoy # if xtoy = (-1, 1) -> x = -1, y = 1
    minD = np.min(actualData)
    maxD = np.max(actualData)
    normalizeData = x + (y - x) * ((actualData - minD) / (maxD - minD))
    return normalizeData

 
                                        ## ## ## QUESTION 1 ## ## ##
# ## # a) IMAGE DATA
# -------------------------------------------------------
# Load Random Images
rnd_list = [os.path.join(imgPath, imgFiles[genRandom(seed=j, fromVal=0, toVal=len(imgFiles) - 1)]) for j in range(4)]
selRandImg = [os.path.join(i, os.listdir(i)[genRandom(fromVal=0, toVal=len(os.listdir(i)) - 1)]) for i in rnd_list]
load_images = [Image.open(img) for img in selRandImg]

# Convert to Grayscale Images
grayScaleImages = [img.convert('L') for img in load_images]

# Normalize the Images using `.getdata()` to fetch matrix data and .new
normalizeImages = []
for img in grayScaleImages:
    img_data = list(img.getdata())
    norm_img_data = minMaxNormalizationNA(img_data)
    width, height = img.size
    normalized_img = Image.new('L', (width, height))
    normalized_img.putdata(norm_img_data)
    normalizeImages.append(normalized_img)

# Plot the images: Color Image, Grayscale Image, Normalized Image, Unnormalized Image
for coIm, grIm, noIm, nnIm in zip(load_images, grayScaleImages, normalizeImages, load_images):
    fig, ((axis_1, axis_2), (axis_3, axis_4)) = plt.subplots(nrows=2, ncols=2, figsize=(6, 6))
        
    plotImages(axis_1, coIm, "Color Image")
    plotImages(axis_2, grIm, "Grayscale Image", cmap="gray")
    plotImages(axis_3, noIm, "Normalized Image")
    plotImages(axis_4, nnIm, "Unnormalized Image")
        
    plt.tight_layout()
    plt.show()

# =======================================================

# ## # b) AUDIO DATA
# -------------------------------------------------------
# Normalization for audio
def minMaxNormalizationNAA(actualData, xtoy):
    x, y = xtoy  # if xtoy = (-1, 1) -> x = -1, y = 1
    actualData = [float(value) for value in actualData]
    minD = min(actualData)
    maxD = max(actualData)
    
    normalizeData = [x + (y - x) * ((value - minD) / (maxD - minD)) for value in actualData]
    return normalizeData

rndChosen = [genRandom(seed=i, fromVal=0, toVal=len(audioFiles) - 1) for i in range(4)]

# Load Audio Files
audioLoadData = []
for i in rndChosen:
    sr, audio = wavfile.read(os.path.join(audPath, audioFiles[i]))
    audioLoadData.append((sr, audio))

audioNormalizeData = []
for sr, audio in audioLoadData:
    audioNormalizeData.append(minMaxNormalizationNAA(audio, (-1, 1)))

# Plot Normalized and Unnormalized audio file data 
for i in range(4):
    unnormalized_audio = audioLoadData[i][1]
    normalized_audio = audioNormalizeData[i]
    sample_rate = audioLoadData[i][0]
    
    time_axis = [j / sample_rate for j in range(len(unnormalized_audio))]

    plt.figure(figsize=(14, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time_axis, unnormalized_audio, label="Unnormalized Audio", color='blue')
    plt.title('Unnormalized Audio Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(time_axis, normalized_audio, label="Normalized Audio (-1, 1)", color='green')
    plt.title('Normalized Audio Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (Normalized)')

    plt.tight_layout()
    plt.show()
                                        ## ## ## QUESTION 2 ## ## ##

# Sequential Sampler
def seqSampler(clsSample):
    samples = [(value, key) for key, value in clsSample.items()]

    def mergeSort(samples):
        if len(samples) <= 1:
            return samples

        mid = len(samples) // 2
        leftH = mergeSort(samples[:mid])
        rightH = mergeSort(samples[mid:])

        return combine(leftH, rightH)

    def combine(left, right):
        sortedSamples = []
        i = j = 0

        while i < len(left) and j < len(right):
            if (-left[i][0], left[i][1]) < (-right[j][0], right[j][1]):
                sortedSamples.append(left[i])
                i += 1
            else:
                sortedSamples.append(right[j])
                j += 1

        sortedSamples.extend(left[i:])
        sortedSamples.extend(right[j:])
        return sortedSamples
    
    return mergeSort(samples)

# Weighted Random Sampler
def weightedRandSampler():
    pass


# Distributed Sampler
def distSamplers(datasets, samples, dtType, noSets=5):
    listOfSets = []
    if dtType == 'image':
        for i in range(noSets):
            dictDistSamp = {}
            for key in samples:
                tempPath = os.path.join(datasets, key)
                dictDistSamp[key] = os.path.join(tempPath, os.listdir(tempPath)[i])
            listOfSets.append(dictDistSamp)
    
    elif dtType == 'audio':
        for i in range(noSets):
            dictDistSamp = {}
            for key in samples:
                audio_files = [f for f in os.listdir(datasets) if f.split('_')[-1].split('.')[0]==key]
                if i < len(audio_files):
                    dictDistSamp[key] = os.path.join(datasets, audio_files[i])
            listOfSets.append(dictDistSamp)
    
    return listOfSets

def samplerStrategy(noSamples, datasets, datasetType, samplerStrategy):
    if datasetType=='audio':
        listSamples = os.listdir(datasets)
        clsNames = [file.split('_')[-1].split('.')[0] for file in listSamples]
        clsCounts = dict(Counter(clsNames))
        # print(clsCounts)
    
    elif datasetType=='image':
        clsNames = os.listdir(datasets)
        clsCounts = {}
        for ls in clsNames:
            clsCounts[ls] = len(os.listdir(os.path.join(datasets, ls)))
        # print(clsCounts)
    
    else:
        print("Please Enter Valid Dataset types.")
        return
    
    if samplerStrategy.lower() == 'sequence':
        samImg = []
        seqSam = seqSampler(clsSample=clsCounts)
        for i in range(noSamples):
            samImgDict = {}
            for tp in seqSam:
                _, dataCls = tp
                if datasetType == 'image':
                    tempPath = os.path.join(datasets, dataCls)
                    samImgDict[dataCls] = os.path.join(tempPath, os.listdir(tempPath)[i])
                else:
                    audFiles = [f for f in os.listdir(datasets) if f.split('_')[-1].split('.')[0]==dataCls]
                    samImgDict[dataCls] = os.path.join(datasets, audFiles[i])
            samImg.append(samImgDict)
        return samImg
    
    elif samplerStrategy.lower() == 'distributed':
        return distSamplers(datasets=datasets, samples=clsCounts, dtType=datasetType, noSets=5)
    
    elif samplerStrategy.lower() == 'weighted':
        return weightedRandSampler()

# smp = samplerStrategy(5, audPath, 'audio', 'sequence')
# print(smp)
samplerStrategy(5, audPath, 'audio', 'sequence')


                                        ## ## ## QUESTION 3 ## ## ##

rndImageFiles = [os.path.join(imgPath, imgFiles[rnd.randint(0, len(imgFiles) - 1)]) for _ in range(2)]
rndImages = [os.path.join(imP, os.listdir(imP)[rnd.randint(0, len(os.listdir(imP)) - 1)]) for imP in rndImageFiles]
rndAudio = [os.path.join(audPath, audioFiles[rnd.randint(0, len(audioFiles) - 1)]) for _ in range(2)]
imgArray = [np.asarray(Image.open(img)) for img in rndImages]

# ## # a) IMAGE DATA
# -------------------------------------------------------
def plotImages(axis, img, title, fontSize=12, cmap=None):
    axis.imshow(img, cmap=cmap)
    axis.set_title(title, fontsize=fontSize)
    axis.axis('off')


# FAST Feature Extraction by using HCD(Harris Corner Detection) by using Guassian filter, gradients 
def HCD(imag, thVal=90):
    grdX = np.gradient(imag, axis=0)
    grdY = np.gradient(imag, axis=1)

    xSquare = gaussian_filter(grdX**2, sigma=1)
    ySquare = gaussian_filter(grdY**2, sigma=1)
    xIntoY  = gaussian_filter(grdY * grdX, sigma=1)

    detMatr = xSquare * ySquare - (xIntoY ** 2)
    tracMatr = xSquare + ySquare

    hcdConst = 0.05
    hcdResp = detMatr - hcdConst * (tracMatr ** 2)
    
    # find corner points
    thresValue = np.percentile(hcdResp, thVal)
    cornersPoints = np.argwhere(hcdResp > thresValue)
    return cornersPoints


# SIFT using Difference of Gaussians
def DOG(imag, thVal=95): 
    sigVals = [(.5, 1), (1, 1.5), (1.5, 2)]
    cornerPoints = []  
    
    for sig1, sig2 in sigVals:
        guaImg1 = gaussian_filter(imag, sigma=sig1)
        guaImg2 = gaussian_filter(imag, sigma=sig2)       
        difGuassian = guaImg1 - guaImg2
        scaleCoPoints = np.argwhere(np.abs(difGuassian) > np.percentile(np.abs(difGuassian), thVal))
        cornerPoints.append(scaleCoPoints)
        
    if cornerPoints:
        cornerPoints = np.vstack(cornerPoints)
    else:
        cornerPoints = np.array([])  
    return cornerPoints


featureExtraction = []
for iArr in imgArray:
    feExFAST = HCD(iArr)
    feExSIFT = DOG(iArr)
    featureExtraction.append((feExFAST, feExSIFT))


fig, axs = plt.subplots(len(imgArray), 2, figsize=(8, 8))
for idx, (img, (fast, sift)) in enumerate(zip(imgArray, featureExtraction)):
    plotImages(axs[idx, 0], img, title=f"Image {idx+1} (FAST)", cmap='gray')
    if fast.size > 0:
        axs[idx, 0].scatter(fast[:, 1], fast[:, 0], color='red', s=5)  

    plotImages(axs[idx, 1], img, title=f"Image {idx+1} (SIFT)", cmap='gray')
    if sift.size > 0:
        axs[idx, 1].scatter(sift[:, 1], sift[:, 0], color='cyan', s=5)  

plt.tight_layout()
plt.show()

# =======================================================

# ## # b) AUDIO DATA
# -------------------------------------------------------
def plotImages(axis, img, title, fontSize=12, cmap=None):
    cax = axis.imshow(img, aspect='auto', cmap=cmap)
    axis.set_title(title, fontsize=fontSize)
    axis.set_xlabel('Frames')
    axis.set_ylabel('Cepstral Coefficients')
    axis.grid(False)
    fig.colorbar(cax, ax=axis, orientation='vertical')

def frammingAudioSignal(signal, frameSize, frameStride, sr):
    frameLen = int(frameSize * sr)
    frameSteps = int(frameStride * sr)
    signalLen = len(signal)
    noFrames = int(np.ceil(float(np.abs(signalLen - frameLen)) / frameSteps))
    pad_signalLen = noFrames * frameSteps + frameLen
    z = np.zeros((pad_signalLen - signalLen))
    pad_signal = np.append(signal, z)
    indices = np.tile(np.arange(0, frameLen), (noFrames, 1)) + \
              np.tile(np.arange(0, noFrames * frameSteps, frameSteps), (frameLen, 1)).T
    frames = pad_signal[indices.astype(np.int32, copy=False)]
    return frames

# Calculate MFCC Here
def calcMFCC(sr, NFFT, noFilter, lowFreq=0, highFreq=None):
    if highFreq is None:
        highFreq = sr // 2
    lowMelCalc = 2595 * np.log10(1 + lowFreq / 700)
    highMelCalc = 2595 * np.log10(1 + highFreq / 700)
    mfccPoints = np.linspace(lowMelCalc, highMelCalc, noFilter + 2)
    freqPoints = 700 * (10**(mfccPoints / 2595) - 1)
    bins = np.floor((NFFT + 1) * freqPoints / sr).astype(int)
    filterbank = np.zeros((noFilter, int(NFFT // 2 + 1)))
    for m in range(1, noFilter + 1):
        f_m_minus = bins[m - 1]
        f_m = bins[m]
        f_m_plus = bins[m + 1]
        for k in range(f_m_minus, f_m):
            filterbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
        for k in range(f_m, f_m_plus):
            filterbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
    return filterbank


# Calculate LFCC Here
def calcLFCC(sr, NFFT, noFilter, lowFreq=0, highFreq=None):
    if highFreq is None:
        highFreq = sr // 2
    freqPoints = np.linspace(lowFreq, highFreq, noFilter + 2)
    bins = np.floor((NFFT + 1) * freqPoints / sr).astype(int)
    filterbank = np.zeros((noFilter, int(NFFT // 2 + 1)))
    for m in range(1, noFilter + 1):
        f_m_minus = bins[m - 1]
        f_m = bins[m]
        f_m_plus = bins[m + 1]
        for k in range(f_m_minus, f_m):
            filterbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
        for k in range(f_m, f_m_plus):
            filterbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
    return filterbank

# Calculate ceptral Coefficient Here
noFilters = 26  
nfft = 512      
noCeptrals = 12 
frameSize = 0.025 
frameStride = 0.01


fig, axes = plt.subplots(2, 2, figsize=(12, 6))
for i, func in enumerate([calcLFCC, calcMFCC]):
    for j, file in enumerate(rndAudio):
        sr, signal = wavfile.read(file)
        empSignal = np.append(signal[0], signal[1:] - 0.97 * signal[:-1])
        frames = frammingAudioSignal(empSignal, frameSize, frameStride, sr)
        frames = frames * get_window('hamming', (int(frameSize * sr)), fftbins=True)
        powSpect = (1.0 / nfft) * ((np.absolute(fft(frames, nfft))) ** 2)
        filtBank = func(sr, nfft, noFilters)
        powSpect = powSpect[:, :filtBank.shape[1]] 
        featExt = np.dot(powSpect, filtBank.T)
        featExt = np.where(featExt == 0, np.finfo(float).eps, featExt)
        logEner = np.log(featExt)
        cepstrals = dct(logEner, type=2, axis=1, norm='ortho')[:, :noCeptrals]
        plotImages(axes[i, j], cepstrals.T, f'{"LFCC" if func == calcLFCC else "MFCC"} - {file}', cmap='viridis')

plt.tight_layout()
plt.show()


## ## ## QUESTION 4 ## ## ##

class DataLoader:
    folderPath = ""
    samplingStrategy = ""
    noSamples = 0
        
    def __init__(self, datasets, samplingStrategy, datasetType, noSamples):
        self.datasets = datasets
        self.samplingStrategy = samplingStrategy
        self.noSamples = noSamples
        self.datasetType = datasetType
        self.datas = self.loadData()
    
    
    def loadData(self):
        if self.datasetType=='audio':
            listSamples = os.listdir(self.datasets)
            clsNames = [file.split('_')[-1].split('.')[0] for file in listSamples]
            clsCounts = dict(Counter(clsNames))
            # print(clsCounts)
        
        elif self.datasetType=='image':
            clsNames = os.listdir(self.datasets)
            clsCounts = {}
            for ls in clsNames:
                clsCounts[ls] = len(os.listdir(os.path.join(self.datasets, ls)))
            # print(clsCounts)
        
        else:
            print("Please Enter Valid Dataset types.")
            return
        
        if self.samplingStrategy.lower() == 'sequence':
            samImg = []
            seqSam = seqSampler(clsSample=clsCounts)
            for i in range(self.noSamples):
                samImgDict = {}
                for tp in seqSam:
                    _, dataCls = tp
                    if self.datasetType == 'image':
                        tempPath = os.path.join(self.datasets, dataCls)
                        samImgDict[dataCls] = os.path.join(tempPath, os.listdir(tempPath)[i])
                    else:
                        audFiles = [f for f in os.listdir(self.datasets) if f.split('_')[-1].split('.')[0]==dataCls]
                        samImgDict[dataCls] = os.path.join(self.datasets, audFiles[i])
                samImg.append(samImgDict)
            return samImg
        
        elif self.samplingStrategy.lower() == 'distributed':
            return distSamplers(samples=clsCounts, noSets=5)
        
        elif self.samplingStrategy.lower() == 'weighted':
            return weightedRandSampler()

    # Sequential Sampler
    def seqSampler(self, clsSample):
        samples = [(value, key) for key, value in clsSample.items()]

        def mergeSort(samples):
            if len(samples) <= 1:
                return samples

            mid = len(samples) // 2
            leftH = mergeSort(samples[:mid])
            rightH = mergeSort(samples[mid:])

            return combine(leftH, rightH)

        def combine(left, right):
            sortedSamples = []
            i = j = 0

            while i < len(left) and j < len(right):
                if (-left[i][0], left[i][1]) < (-right[j][0], right[j][1]):
                    sortedSamples.append(left[i])
                    i += 1
                else:
                    sortedSamples.append(right[j])
                    j += 1

            sortedSamples.extend(left[i:])
            sortedSamples.extend(right[j:])
            return sortedSamples
        
        return mergeSort(samples)

    # Weighted Random Sampler
    def weightedRandSampler(self):
        pass

    # Distributed Sampler
    def distSamplers(self, samples, noSets=5):
        listOfSets = []
        if self.datasetType == 'image':
            for i in range(noSets):
                dictDistSamp = {}
                for key in samples:
                    tempPath = os.path.join(self.datasets, key)
                    dictDistSamp[key] = os.path.join(tempPath, os.listdir(tempPath)[i])
                listOfSets.append(dictDistSamp)
        
        elif self.datasetType == 'audio':
            for i in range(noSets):
                dictDistSamp = {}
                for key in samples:
                    audio_files = [f for f in os.listdir(self.datasets) if f.split('_')[-1].split('.')[0]==key]
                    if i < len(audio_files):
                        dictDistSamp[key] = os.path.join(self.datasets, audio_files[i])
                listOfSets.append(dictDistSamp)
        
        return listOfSets
    
    
    # For Image Datasets
    def toGrayScaleImg(self, img):
        img = Image.open(img)
        toGrayImage = img.convert('L')
        return toGrayImage
    
    def minMaxNormalization(self, types, actualData, xtoy=(-1, 1)):
        x, y = xtoy # if xtoy = (-1, 1) -> x = -1,  y = 1
        if types == "Audio":
            actualData = [float(value) for value in actualData]
        elif types == "Image":
            actualData = [value for value in actualData]
            
        minD = np.min(actualData)
        maxD = np.max(actualData)
        
        normalizeData = x + (y - x) * ((actualData - minD) / (maxD - minD))
        return normalizeData
    
    # FAST Feature Extraction by using HCD(Harris Corner Detection) by using Guassian filter, gradients 
    def HCD(imag, thVal=95):
        grdX = np.gradient(imag, axis=0)
        grdY = np.gradient(imag, axis=1)

        xSquare = gaussian_filter(grdX**2, sigma=1)
        ySquare = gaussian_filter(grdY**2, sigma=1)
        xIntoY  = gaussian_filter(grdY * grdX, sigma=1)

        detMatr = xSquare * ySquare - (xIntoY ** 2)
        tracMatr = xSquare + ySquare

        hcdConst = 0.05
        hcdResp = detMatr - hcdConst * (tracMatr ** 2)
        
        # find corner points
        thresValue = np.percentile(hcdResp, thVal)
        cornersPoints = np.argwhere(hcdResp > thresValue)
        return cornersPoints


    # SIFT using Difference of Gaussians
    def DOG(imag, thVal=99): 
        sigVals = [(.5, 1), (1, 1.5), (1.5, 2)]
        cornerPoints = []  
        
        for sig1, sig2 in sigVals:
            guaImg1 = gaussian_filter(imag, sigma=sig1)
            guaImg2 = gaussian_filter(imag, sigma=sig2)       
            difGuassian = guaImg1 - guaImg2
            scaleCoPoints = np.argwhere(np.abs(difGuassian) > np.percentile(np.abs(difGuassian), thVal))
            cornerPoints.append(scaleCoPoints)
            
        if cornerPoints:
            cornerPoints = np.vstack(cornerPoints)
        else:
            cornerPoints = np.array([])  
        return cornerPoints

    
    # Plot Images
    def plotImageData(self, axis, img, title, fontSize=12, cmap=None):
        axis.imshow(img, cmap=cmap)
        axis.set_title(title, fontsize=fontSize)
        axis.axis('off')
        
    def plotAudioData(self, axis, img, title, fontSize=12, cmap=None):
        cax = axis.imshow(img, aspect='auto', cmap=cmap)
        axis.set_title(title, fontsize=fontSize)
        axis.set_xlabel('Frames')
        axis.set_ylabel('Cepstral Coefficients')
        axis.grid(False)
        fig.colorbar(cax, ax=axis, orientation='vertical')
        
    def preprocessImage(self, datasets):
        preprocessDatasets = {'Original Data': [], 'Normalized Data': [], 'GrayScale Data': []}
        for image in datasets:
            preprocessDatasets['Original Data'].append(Image.open(image))
            preprocessDatasets['Normalized Data'].append(self.minMaxNormalization("Image", np.asarray(Image.open(image))))
            preprocessDatasets['GrayScale Data'].append(self.toGrayScaleImg(image))

        return preprocessDatasets
    
    # For Audio Datasets
    def frammingAudioSignal(self, signal, frameSize, frameStride, sr):
        frameLen = int(frameSize * sr)
        frameSteps = int(frameStride * sr)
        signalLen = len(signal)
        noFrames = int(np.ceil(float(np.abs(signalLen - frameLen)) / frameSteps))
        pad_signalLen = noFrames * frameSteps + frameLen
        z = np.zeros((pad_signalLen - signalLen))
        pad_signal = np.append(signal, z)
        indices = np.tile(np.arange(0, frameLen), (noFrames, 1)) + \
                np.tile(np.arange(0, noFrames * frameSteps, frameSteps), (frameLen, 1)).T
        frames = pad_signal[indices.astype(np.int32, copy=False)]
        return frames

    # Calculate MFCC Here
    def calcMFCC(self, sr, NFFT, noFilter, lowFreq=0, highFreq=None):
        if highFreq is None:
            highFreq = sr // 2
        lowMelCalc = 2595 * np.log10(1 + lowFreq / 700)
        highMelCalc = 2595 * np.log10(1 + highFreq / 700)
        mfccPoints = np.linspace(lowMelCalc, highMelCalc, noFilter + 2)
        freqPoints = 700 * (10**(mfccPoints / 2595) - 1)
        bins = np.floor((NFFT + 1) * freqPoints / sr).astype(int)
        filterbank = np.zeros((noFilter, int(NFFT // 2 + 1)))
        for m in range(1, noFilter + 1):
            f_m_minus = bins[m - 1]
            f_m = bins[m]
            f_m_plus = bins[m + 1]
            for k in range(f_m_minus, f_m):
                filterbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
            for k in range(f_m, f_m_plus):
                filterbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
        return filterbank


    # Calculate LFCC Here
    def calcLFCC(self, sr, NFFT, noFilter, lowFreq=0, highFreq=None):
        if highFreq is None:
            highFreq = sr // 2
        freqPoints = np.linspace(lowFreq, highFreq, noFilter + 2)
        bins = np.floor((NFFT + 1) * freqPoints / sr).astype(int)
        filterbank = np.zeros((noFilter, int(NFFT // 2 + 1)))
        for m in range(1, noFilter + 1):
            f_m_minus = bins[m - 1]
            f_m = bins[m]
            f_m_plus = bins[m + 1]
            for k in range(f_m_minus, f_m):
                filterbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
            for k in range(f_m, f_m_plus):
                filterbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
        return filterbank

    def preprocessAudio(self, datasets):            
        preprocessDatasets = {'Original Data': [], 'Normalized Data': [], 'MFCC Data': [], 'LFCC Data': []}
        # Calculate ceptral Coefficient Here
        noFilters = 26  
        nfft = 512      
        noCeptrals = 12 
        frameSize = 0.025 
        frameStride = 0.01
        
        for i, func in enumerate([self.calcLFCC, self.calcMFCC]):
            for j, file in enumerate(datasets):
                sr, signal = wavfile.read(file)
                empSignal = np.append(signal[0], signal[1:] - 0.97 * signal[:-1])
                frames = self.frammingAudioSignal(empSignal, frameSize, frameStride, sr)
                frames = frames * get_window('hamming', (int(frameSize * sr)), fftbins=True)
                powSpect = (1.0 / nfft) * ((np.absolute(fft(frames, nfft))) ** 2)
                filtBank = func(sr, nfft, noFilters)
                powSpect = powSpect[:, :filtBank.shape[1]] 
                featExt = np.dot(powSpect, filtBank.T)
                featExt = np.where(featExt == 0, np.finfo(float).eps, featExt)
                logEner = np.log(featExt)
                cepstrals = dct(logEner, type=2, axis=1, norm='ortho')[:, :noCeptrals]

                preprocessDatasets['Original Data'].append((sr, signal))
                preprocessDatasets['Normalized Data'].append((sr, self.minMaxNormalization("Audio", signal)))
                if i == 0:
                    preprocessDatasets['LFCC Data'].append(cepstrals)
                else:
                    preprocessDatasets['MFCC Data'].append(cepstrals)
                    
        return preprocessDatasets


imgLoader = DataLoader(imgPath, "Sequence", 'image', 1)
audLoader = DataLoader(audPath, "sequence", 'audio', 1)
imgData = imgLoader.datas
audData = audLoader.datas

images = []
for imSet in imgData:
    images.extend(imSet.values())

audios = []
for audSet in audData:
    audios.extend(audSet.values())


proceImageData = imgLoader.preprocessImage(images[:4])
proceAudioData = imgLoader.preprocessAudio(audios[:4])
# print(proceAudioData)

for coIm, grIm, noIm, nnIm in zip(proceImageData['Original Data'], proceImageData['GrayScale Data'], proceImageData['Normalized Data'], proceImageData['Original Data']):
    fig, ((axis_1, axis_2), (axis_3, axis_4)) = plt.subplots(nrows=2, ncols=2, figsize=(6, 6))
        
    imgLoader.plotImageData(axis_1, coIm, "Color Image")
    imgLoader.plotImageData(axis_2, grIm, "Grayscale Image", cmap="gray")
    imgLoader.plotImageData(axis_3, noIm, "Normalized Image")
    imgLoader.plotImageData(axis_4, np.asarray(nnIm), "Unnormalized Image")
        
    plt.tight_layout()
    plt.show()
    

for orData, normData, audio_data1, audio_data2 in zip(
    proceAudioData['Original Data'], 
    proceAudioData['Normalized Data'], 
    proceAudioData['MFCC Data'], 
    proceAudioData['LFCC Data']
):
    sr, signal = orData  # Unpack sample rate and signal
    time_axis = np.linspace(0, len(signal) / sr, num=len(signal))  # Use signal length

    plt.figure(figsize=(14, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time_axis, signal, label="Unnormalized Audio", color='blue')  # Use 'signal' instead of orData[1]
    plt.title('Unnormalized Audio Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(time_axis, normData[1], label="Normalized Audio (-1, 1)", color='green')  # Ensure normData is correctly indexed
    plt.title('Normalized Audio Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (Normalized)')
    
    plt.tight_layout()
    plt.show()
    
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    audLoader.plotAudioData(axs[0], audio_data1, "MFCC Data")
    audLoader.plotAudioData(axs[1], audio_data2, "LFCC Data")
    
    plt.tight_layout()
    plt.show()


#########################################################
#####################  INTERMEDIATE  ####################
#########################################################

# a)
class DataLoaderPipeline:
    def __init__(self, datasets, datasetType, noSamples):
        self.datasets = datasets
        self.datasetType = datasetType
        self.noSamples = noSamples
        
    def loadData(self):
        if self.datasetType=='audio':
            listSamples = os.listdir(self.datasets)
            clss = list(set([file.split('_')[-1].split('.')[0] for file in listSamples]))
            print(clss)
            dataSamples = []
            labels = []
            for i, path in enumerate(listSamples):
                dataSamples.append(os.path.join(self.datasets, path))
                labels.append(clss.index(path.split('_')[-1].split('.')[0]))
                
            return dataSamples[:self.noSamples], labels[:self.noSamples]
        
        elif self.datasetType=='image':
            clsPath = [os.path.join(self.datasets, clsp) for clsp in os.listdir(self.datasets)]

            imgs = [os.path.join(clsp, imgp) for clsp in clsPath for imgp in os.listdir(clsp)[:int(self.noSamples/len(clsPath))]]
            clss = [i for i, clsp in enumerate(clsPath) for _ in os.listdir(clsp)]
            
            imgArray = []
            labels = []
            for j in range(self.noSamples):
                img = Image.open(imgs[j])
                img = img.convert('RGB')
                img = np.asarray(img)
                imgArray.append(img)
                labels.append(clss[j])
            
            return imgArray, labels
        
        else:
            print("Please Enter Valid Dataset types.")
            return None

class FeatureExtraction:
    def __init__(self, method, loadedData):
        self.loadedData = loadedData
        self.method = method
        
    ## ## Extraction of Audio features
    # For Audio Datasets
    def frammingAudioSignal(self, signal, frameSize, frameStride, sr):
        frameLen = int(frameSize * sr)
        frameSteps = int(frameStride * sr)
        signalLen = len(signal)
        noFrames = int(np.ceil(float(np.abs(signalLen - frameLen)) / frameSteps))
        pad_signalLen = noFrames * frameSteps + frameLen
        z = np.zeros((pad_signalLen - signalLen))
        pad_signal = np.append(signal, z)
        indices = np.tile(np.arange(0, frameLen), (noFrames, 1)) + \
                np.tile(np.arange(0, noFrames * frameSteps, frameSteps), (frameLen, 1)).T
        frames = pad_signal[indices.astype(np.int32, copy=False)]
        return frames

    # Calculate MFCC Here
    def calcMFCC(self, sr, NFFT, noFilter, lowFreq=0, highFreq=None):
        if highFreq is None:
            highFreq = sr // 2
        lowMelCalc = 2595 * np.log10(1 + lowFreq / 700)
        highMelCalc = 2595 * np.log10(1 + highFreq / 700)
        mfccPoints = np.linspace(lowMelCalc, highMelCalc, noFilter + 2)
        freqPoints = 700 * (10**(mfccPoints / 2595) - 1)
        bins = np.floor((NFFT + 1) * freqPoints / sr).astype(int)
        filterbank = np.zeros((noFilter, int(NFFT // 2 + 1)))
        for m in range(1, noFilter + 1):
            f_m_minus = bins[m - 1]
            f_m = bins[m]
            f_m_plus = bins[m + 1]
            for k in range(f_m_minus, f_m):
                filterbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
            for k in range(f_m, f_m_plus):
                filterbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
        return filterbank


    # Calculate LFCC Here
    def calcLFCC(self, sr, NFFT, noFilter, lowFreq=0, highFreq=None):
        if highFreq is None:
            highFreq = sr // 2
        freqPoints = np.linspace(lowFreq, highFreq, noFilter + 2)
        bins = np.floor((NFFT + 1) * freqPoints / sr).astype(int)
        filterbank = np.zeros((noFilter, int(NFFT // 2 + 1)))
        for m in range(1, noFilter + 1):
            f_m_minus = bins[m - 1]
            f_m = bins[m]
            f_m_plus = bins[m + 1]
            for k in range(f_m_minus, f_m):
                filterbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
            for k in range(f_m, f_m_plus):
                filterbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
        return filterbank
    
    def preprocessAudio(self, labels):            
        preprocessDatasets = []
        noFilters = 26  
        nfft = 512      
        noCeptrals = 12 
        frameSize = 0.035 
        frameStride = 0.03
        
        if self.method == 'lfcc':
            for j, file in enumerate(self.loadedData):
                try:
                    sr, signal = wavfile.read(file)
                    if len(signal) == 0:  # Check if signal is empty
                        print(f"Empty or invalid file: {file}")
                        labels.pop(j)
                        continue
                    
                    empSignal = np.append(signal[0], signal[1:] - 0.97 * signal[:-1])
                    frames = self.frammingAudioSignal(empSignal, frameSize, frameStride, sr)
                    frames = frames * get_window('hamming', (int(frameSize * sr)), fftbins=True)
                    powSpect = (1.0 / nfft) * ((np.absolute(fft(frames, nfft))) ** 2)
                    filtBank = self.calcLFCC(sr, nfft, noFilters)
                    powSpect = powSpect[:, :filtBank.shape[1]] 
                    featExt = np.dot(powSpect, filtBank.T)
                    featExt = np.where(featExt == 0, np.finfo(float).eps, featExt)
                    logEner = np.log(featExt)
                    cepstrals = dct(logEner, type=2, axis=1, norm='ortho')[:, :noCeptrals]
                    
                    preprocessDatasets.append(cepstrals)
                    
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
                    continue
                    
        elif self.method == 'mfcc':
            for j, file in enumerate(self.loadedData):
                try:
                    sr, signal = wavfile.read(file)
                    if len(signal) == 0:  # Check if signal is empty
                        print(f"Empty or invalid file: {file}")
                        labels.pop(j)
                        continue
                    
                    empSignal = np.append(signal[0], signal[1:] - 0.97 * signal[:-1])
                    frames = self.frammingAudioSignal(empSignal, frameSize, frameStride, sr)
                    frames = frames * get_window('hamming', (int(frameSize * sr)), fftbins=True)
                    powSpect = (1.0 / nfft) * ((np.absolute(fft(frames, nfft))) ** 2)
                    filtBank = self.calcMFCC(sr, nfft, noFilters)
                    powSpect = powSpect[:, :filtBank.shape[1]] 
                    featExt = np.dot(powSpect, filtBank.T)
                    featExt = np.where(featExt == 0, np.finfo(float).eps, featExt)
                    logEner = np.log(featExt)
                    cepstrals = dct(logEner, type=2, axis=1, norm='ortho')[:, :noCeptrals]
                    
                    preprocessDatasets.append(cepstrals)
                    
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
                    continue
                        
        return preprocessDatasets


    ## ## Extraction of Image features
    # # FAST Feature Extraction by using HCD(Harris Corner Detection) by using Guassian filter, gradients 
    def HCD(self, imag, thVal=95):        
        grdX = np.gradient(imag, axis=0)
        grdY = np.gradient(imag, axis=1)

        xSquare = gaussian_filter(grdX**2, sigma=1)
        ySquare = gaussian_filter(grdY**2, sigma=1)
        xIntoY  = gaussian_filter(grdY * grdX, sigma=1)

        detMatr = xSquare * ySquare - (xIntoY ** 2)
        tracMatr = xSquare + ySquare

        hcdConst = 0.05
        hcdResp = detMatr - hcdConst * (tracMatr ** 2)
        
        thresValue = np.percentile(hcdResp, thVal)
        print(f"HCD threshold value: {thresValue}")
        
        cornersPoints = np.argwhere(hcdResp > thresValue)
        return cornersPoints

    # # SIFT using Difference of Gaussians
    def DOG(self, imag, thVal=96):
        
        sigVals = [(.5, 1), (1, 1.5), (1.5, 2)]
        cornerPoints = []  
        
        for sig1, sig2 in sigVals:
            guaImg1 = gaussian_filter(imag, sigma=sig1)
            guaImg2 = gaussian_filter(imag, sigma=sig2)       
            difGuassian = guaImg1 - guaImg2
            
            
            scaleCoPoints = np.argwhere(np.abs(difGuassian) > np.percentile(np.abs(difGuassian), thVal))
            cornerPoints.append(scaleCoPoints)
        
        if cornerPoints:
            cornerPoints = np.vstack(cornerPoints)
        else:
            cornerPoints = np.array([])
        
        return cornerPoints

    # Preprocessing the image data
    def preprocessImage(self):
        preprocessDatasets = []
        
        for i, img in enumerate(self.loadedData):
            if not isinstance(img, np.ndarray):
                print("NO")
                img = np.asarray(Image.open(img))

            if self.method.lower() == 'shift':
                preprocessDatasets.append(self.DOG(img))
            elif self.method.lower() == 'fast':
                preprocessDatasets.append(self.HCD(img))

        return preprocessDatasets

    
class TrainingModel:
    def __init__(self, datas, targets, testSize=0.4):
        self.datas = datas
        self.targets = targets
        self.testSize = testSize
        
        
    def trainModel(self):
        max_shape = tuple(max(s) for s in zip(*[f.shape for f in self.datas]))
        features = np.array([np.pad(f, [(0, max_shape[i] - f.shape[i]) for i in range(len(f.shape))], mode='constant', constant_values=0) for f in self.datas])
        xTrain, xTest, yTrain, yTest = train_test_split(features, self.targets, test_size=self.testSize, random_state=42)

        modelTypes = [("LinearRegression", LinearRegression()), ("RidgeRegression", Ridge()), ("LassoRegression", Lasso())]
        
        xTrain_flat = xTrain.reshape(xTrain.shape[0], -1)
        for modelName, model in modelTypes:
            model.fit(xTrain_flat, yTrain)
            preds = model.predict(xTest.reshape(xTest.shape[0], -1))
            mse = mean_squared_error(yTest, preds)
            
            print(f"{modelName}: {mse}")
            
audPath = 'Datasets/MLA2_DATA/AUDIO'
dtPipeline = DataLoaderPipeline(imgPath, 'image', 1000)
samples, labels = dtPipeline.loadData()

featureExtract = FeatureExtraction('fast', samples)
audioFeature = featureExtract.preprocessImage()

print(len(audioFeature))
audioFeatures = [feature.flatten() for feature in audioFeature]

trainModel = TrainingModel(audioFeature, labels)
trainModel.trainModel()
