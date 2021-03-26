import random
import string
import time
import wave
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import numpy
import numpy as np
import scipy.io.wavfile
#import sounddevice as sd
from Crypto.Cipher import AES
# import of AES:
from scipy.io import wavfile
from tqdm import tqdm

# TODO random.randint() from Enaudio.py

audio_window = Tk()
audio_window.geometry('360x200')
audio_window.title('Audio Cryptography')


def goback():
    exit()


def powmod(b, e, m):
    b2 = b
    res = 1
    while e:
        if e & 1:
            res = (res * b2) % m
        b2 = (b2 * b2) % m
        e >>= 1
    return res


def filenameerror():
    messagebox.showinfo('Error Occured!', 'Please select a 16bit mono or stereo audio file')


def enfinish16():
    messagebox.showinfo('Done!', 'Encryption is Finished and saved as RSA_Encrypted_NEG.wav and RSA_Encrypted_POS.wav')


def encryptaes():
    messagebox.showinfo('Done!', 'Encryption is Finished and saved as AES_Encrypted.wav')


def decryptfinishaes():
    messagebox.showinfo('Done!', 'Decryption is finished and saved as AES_Decrypted.wav')


def definish():
    messagebox.showinfo('Done!', 'Decryption is finished and saved as RSA_Decrypted.wav')


def sixteen_encrypt():
    try:
        start = time.time() #lấy thời gian bắt đầu chạy ctrinh
        filename = askopenfilename() #để mở file
        foo = wave.open(filename, 'rb')
        channels = foo.getnchannels()
        fsrate = foo.getframerate()
        # print(channels)

        if channels == 2:  # stereo

            # Encryption

            fs, data = scipy.io.wavfile.read(filename)
            print('The original data: \n', +data)
            print('The frame rate: ', +fs)
            # print(type(data))
            a, b = data.shape
            tup = (a, b)
            data = data.astype(numpy.int16)  # 16
            # data = numpy.asarray(data, dtype=numpy.int16)
            # print(data.flags)
            data.setflags(write=1)
            # print(data.flags)
            # print((a,b))
            Time = numpy.linspace(0, len(data) / fs, num=len(data))
            plt.figure(1)
            plt.title('Original Signal Wave')
            plt.plot(Time, data)
            plt.savefig('Original.png')

            posdata = numpy.where(data >= 0, data, -1)  # -640292407 -(n)
            negdata = numpy.where(data <= 0, data, 1)  # 640292407 (n)
            print('The array made from the positive datas: \n', +posdata)
            print('The array made from the negativetive datas: \n', +negdata)

            for i in range(0, tup[0]):
                for j in range(0, tup[1]):
                    if posdata[i][j] == -1 or negdata[i][j] < 0:
                        x = negdata[i][j]  #gan mang data cho x
                        x = ((pow(x, 65537)) % 31243) #Encrypt = (data^e) % n
                        negdata[i][j] = x
                    elif posdata[i][j] > 0 or negdata[i][j] == 1:
                        x = posdata[i][j]
                        x = ((pow(x, 65537)) % 31243)
                        posdata[i][j] = x
                    else:
                        posdata[i][j] = 0
                        negdata[i][j] = posdata[i][j]

            print('\n Encrypted positive array:')
            print(posdata)
            print('\n Encrypted negative array:')
            print(negdata)
            print('\n')
            scipy.io.wavfile.write('RSA_Encrypted_POS.wav', fs, posdata)
            scipy.io.wavfile.write('RSA_Encrypted_NEG.wav', fs, negdata)

            Time = numpy.linspace(0, len(posdata) / fs, num=len(posdata))
            plt.figure(2)
            plt.title('Encrypted Signal Wave')
            plt.plot(Time, posdata)
            plt.savefig('posdata.png')

            Time = numpy.linspace(0, len(negdata) / fs, num=len(negdata))
            plt.figure(3)
            plt.title('Encrypted Signal Wave')
            plt.plot(Time, negdata)
            plt.savefig('negdata.png')

            end = time.time()
            ElspTime = (end - start)
            print('\n Sorry for taking', +ElspTime, 'sec from your life!')

        else:  # mono

            binarySound = {}
            binaryHeader = {}

            song = {}

            # dt = numpy.dtype(int)
            # dt = dt.newbyteorder('>')
            # numpy.frombuffer(buffer, dtype=dt)

            with open(filename, 'rb') as f:
                dt = numpy.dtype(int)
                dt = dt.newbyteorder('>')
                buffer = f.read(44)
                # print(type(buffer))
                binaryHeader = numpy.frombuffer(buffer, dtype=numpy.int16)  # TODO remove the file header
                buffer = f.read()
                binarySound = numpy.frombuffer(buffer, dtype=numpy.int16)
            # Encryption

            framerate = fsrate
            data = binarySound
            print('The original data: \n', +data)
            print('The frame rate: ', +framerate)

            Time = numpy.linspace(0, len(data) / framerate, num=len(data))
            plt.figure(1)
            plt.title('Original Signal Wave')
            plt.plot(Time, data)
            plt.savefig('Original.png')

            posdata = numpy.where(data >= 0, data, -1)
            negdata = numpy.where(data <= 0, data, 1)

            for i in range(len(data)):
                if posdata[i] == -1 or negdata[i] < 0:
                    x = negdata[i]
                    x = ((pow(x, 65537)) % 31243)
                    negdata[i] = x
                elif posdata[i] > 0 or negdata[i] == 1:
                    x = posdata[i]
                    x = ((pow(x, 65537)) % 31243)
                    posdata[i] = x
                else:
                    posdata[i] = 0
                    negdata[i] = posdata[i]
            print('\n Encrypted positive array:')
            print(posdata)
            print('\n Encrypted negative array:')
            print(negdata)
            print('\n')

            scipy.io.wavfile.write('RSA_Encrypted_POS.wav', framerate, posdata)
            scipy.io.wavfile.write('RSA_Encrypted_NEG.wav', framerate, negdata)

            Time = numpy.linspace(0, len(posdata) / framerate, num=len(posdata))
            plt.figure(2)
            plt.title('Posdata Wave')
            plt.plot(Time, posdata)
            # plt.show()
            plt.savefig('posdata.png')

            Time = numpy.linspace(0, len(negdata) / framerate, num=len(negdata))
            plt.figure(3)
            plt.title('Negdata Wave')
            plt.plot(Time, negdata)
            # plt.show()
            plt.savefig('negdata.png')

            end = time.time()
            ElspTime = (end - start)
            print('\n Sorry for taking', +ElspTime, 'sec from your life!')

        enfinish16()
    except TypeError:
        filenameerror()

    except AttributeError:
        filenameerror()


def sixteen_decrypt():
    try:
        file11 = askopenfilename()
        file22 = askopenfilename()
        file1 = wave.open(file11, 'rb')
        file2 = wave.open(file22, 'rb')
        channel1 = file1.getnchannels()
        fsrate1 = file1.getframerate()
        # channel2 = file2.getnchannels()
        # fsrate2 = file2.getframerate()
        # print(channels)
        start = time.time()

        # TODO if() exception handling of another file format

        if (
                channel1 == 2):  # stereo
            # TODO check if channel1==channel2 #TODO exception handling of selecting 2 diff file

            # Decryption

            fs, data = scipy.io.wavfile.read(file11)
            fs1, data1 = scipy.io.wavfile.read(file22)
            print('The first file:\n', +data)
            print('The second file:\n', +data1)
            # print(type(data))
            # print(type(dataarray))
            a1, b1 = data.shape
            tup1 = (a1, b1)
            data = data.astype(numpy.int16)  # 16
            data1 = data1.astype(numpy.int16)
            # print(data.flags)
            data.setflags(write=1)
            data1.setflags(write=1)
            # print(data.flags)
            # print((a1,b1))
            data = data.tolist()
            data1 = data1.tolist()

            for i1 in tqdm(range(len(data))):
                for j1 in (range(len(data[i1]))):
                    if data[i1][j1] == -1 or data1[i1][j1] < 0:
                        x1 = data1[i1][j1]
                        x1 = powmod(x1, 9305, 31243)  # = ((pow(x1,9305)) % 31243) #decrypt = (data^d) % n
                        x1 = x1 - 31243
                        data[i1][j1] = x1
                    elif data[i1][j1] > 0 or data[i1][j1] == 1:
                        x1 = data[i1][j1]
                        x1 = powmod(x1, 9305, 31243)  # = ((pow(x1,9305)) % 31243)
                        data[i1][j1] = x1
                    else:
                        data[i1][j1] = 0
            data = numpy.array(data).astype(numpy.int16)
            # data = data.astype(numpy.int16)
            #print('The original data: \n', +data)
            scipy.io.wavfile.write('RSA_Decrypted.wav', fsrate1, data)

            end = time.time()
            ElspTime = (end - start)
            print('\n Sorry for taking ', +ElspTime, 'sec from your life!')

        else:

            with open(file11, 'rb') as f:
                dt = numpy.dtype(int)
                dt = dt.newbyteorder('>')
                buffer = f.read(44)
                # print(type(buffer))
                binaryHeader = numpy.frombuffer(buffer, dtype=numpy.int16)  # TODO remove the file header
                buffer = f.read()
                binarySound = numpy.frombuffer(buffer, dtype=numpy.int16)
            data = binarySound
            # fs, data = scipy.io.waffle.read(askopenfilename())
            print('The first file:\n', +data)
            # print(fs)

            with open(file22, 'rb') as f:
                dt = numpy.dtype(int)
                dt = dt.newbyteorder('>')
                buffer = f.read(44)
                # print(type(buffer))
                binaryHeader = numpy.frombuffer(buffer, dtype=numpy.int16)  # TODO remove the file header
                buffer = f.read()
                binarySound = numpy.frombuffer(buffer, dtype=numpy.int16)
            data1 = binarySound
            print('The second file:\n', +data1)

            data = data.tolist()
            data1 = data1.tolist()

            for i1 in tqdm(range(len(data))):
                if data[i1] == -1 or data1[i1] < 0:
                    x1 = data1[i1]
                    x1 = powmod(x1, 9305, 31243)  # = ((pow(x1,9305)) % 31243)
                    x1 = x1 - 31243
                    data[i1] = x1
                elif data[i1] > 0 or data1[i1] == 1:
                    x1 = data[i1]
                    x1 = powmod(x1, 9305, 31243)  # = ((pow(x1,9305)) % 31243)
                    data[i1] = x1
                else:
                    data[i1] = 0

            data = numpy.array(data)
            data = data.astype(numpy.int16)
            print('The original data: \n', +data)
            scipy.io.wavfile.write('RSA_Decrypted.wav', fsrate1, data)

            end = time.time()
            ElspTime = (end - start)
            print('\n Sorry for taking', +ElspTime, 'sec from your life!')
        ############ finish of decryption ##############
        definish()
    except TypeError:
        filenameerror()

    except AttributeError:
        filenameerror()


# ---------------------------------- AES method ---------------------------------------
# Getting ready with AES

AES_KEY = ""
AES_IV = ""


def gettingready_aes():
    global AES_KEY
    # AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
    AES_KEY = 'V0u2Xd1vKsSTpeYc0jwfxe5Wt8umwjVN'

    global AES_IV
    # AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
    AES_IV = 'IknLo7UWHjl9E0vy'


gettingready_aes()


def encrypt_aes():
    # Taking input
    filename_aes = askopenfilename()

    fs, data = wavfile.read(filename_aes)

    plt.plot(data)  # fs = sampling frequency = 44.1kHz
    plt.title("Original Audio Plot")

    with open(filename_aes, 'rb') as fd:
        contents = fd.read()
    # Playing that sound

    #sd.play(data, fs)
    # Getting ready with AES
    print("----------- AES  Encrypt key ------------")
    print("AES Key is ", AES_KEY)
    print("AES Initialization vector is ", AES_IV)
    # Encrpytion of audio file
    encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    encrypted_audio = encryptor.encrypt(contents)

    # Saving the encrypted file
    with open('AES_Encrypted.wav', 'wb') as fd:
        fd.write(encrypted_audio)
    print("A file titled 'AES_Encrypted.wav' is generated which is the encrypted audio to be communicated")
    encryptaes()


def decrypt_aes():
    print("----------- AES Decrypt with key ------------")
    print("AES Key is ", AES_KEY)
    print("AES Initialization vector is ", AES_IV)
    # Loading
    encrypted_aes = askopenfilename()
    with open(encrypted_aes, 'rb') as fd:
        contents1 = fd.read()

    # Decryption of data
    decryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    decrypted_audio = decryptor.decrypt(contents1)

    with open('AES_Decrypted.wav', 'wb') as fd:
        fd.write(decrypted_audio)

    fs, data1 = wavfile.read('AES_Decrypted.wav')
    plt.plot(data1)  # fs = sampling frequency = 44.1kHz
    plt.title("Original Audio Plot")
    data_1 = np.asarray(data1, dtype=np.int32)
    #sd.play(data_1, fs)
    decryptfinishaes()


btn_16_decrypt = Button(audio_window, text="RSA Audio Decryption", command=sixteen_decrypt)
btn_16_decrypt.place(x=10, y=100)

btn_16_encrypt = Button(audio_window, text="RSA Audio Encryption", command=sixteen_encrypt)
btn_16_encrypt.place(x=10, y=50)

btn_AES_decrypt = Button(audio_window, text="AES Audio Decryption", command=decrypt_aes)
btn_AES_decrypt.place(x=180, y=100)

btn_AES_encrypt = Button(audio_window, text="AES Audio Encryption", command=encrypt_aes)
btn_AES_encrypt.place(x=180, y=50)

btn_exit = Button(audio_window, text="Go Back", command=goback).place(x=140, y=150)

audio_window.mainloop()
