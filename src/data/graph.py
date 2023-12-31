import os, sys, csv
sys.path.append("/mnt/e/Program/Python/Colorization")
import matplotlib.pyplot as plt
import numpy as np


def graph_all(output_file):
    cGAN_psnr = []
    cGAN_ssim = []
    CF_psnr = []
    CF_ssim = []
    DISCO_psnr = []
    DISCO_ssim = []
    UGATIT_psnr = []
    UGATIT_ssim = []

    with open(output_file, "r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for line in reader:
            print(line[0])
            cGAN_psnr.append(float(line[1]))
            cGAN_ssim.append(float(line[2]))
            CF_psnr.append(float(line[3]))
            CF_ssim.append(float(line[4]))
            DISCO_psnr.append(float(line[5]))
            DISCO_ssim.append(float(line[6]))
            UGATIT_psnr.append(float(line[7]))
            UGATIT_ssim.append(float(line[8]))
            
    fig = plt.figure("psnr", figsize=(10, 10))
    n = range(len(cGAN_psnr))
    cGAN = fig.add_subplot(411)
    cGAN.plot(n, cGAN_psnr, 'r', label='cGAN')
    print(np.mean(cGAN_psnr))
    CF = fig.add_subplot(412)
    CF.plot(n, CF_psnr, 'g', label='CF')
    print(np.mean(CF_psnr))
    DISCO = fig.add_subplot(413)
    DISCO.plot(n, DISCO_psnr, 'b', label='DISCO')
    print(np.mean(DISCO_psnr))
    UGATIT = fig.add_subplot(414)
    UGATIT.plot(n, UGATIT_psnr, 'y', label='UGATIT')
    print(np.mean(UGATIT_psnr))
    fig.legend(loc='upper right')
    plt.savefig('result/_graph/psnr_TM1.png')
    plt.show()
    
    print('save_psnr')

    fig = plt.figure("ssim", figsize=(10, 10))
    n = range(len(cGAN_ssim))
    cGAN = fig.add_subplot(411)
    cGAN.plot(n, cGAN_ssim, 'r', label='cGAN')
    plt.legend(loc='upper right')
    print(np.mean(cGAN_ssim))
    CF = fig.add_subplot(412)
    CF.plot(n, CF_ssim, 'g', label='CF')
    print(np.mean(CF_ssim))
    DISCO = fig.add_subplot(413)
    DISCO.plot(n, DISCO_ssim, 'b', label='DISCO')
    print(np.mean(DISCO_ssim))
    UGATIT = fig.add_subplot(414)
    UGATIT.plot(n, UGATIT_ssim, 'y', label='UGATIT')
    print(np.mean(UGATIT_ssim))
    fig.legend(loc='upper right')
    plt.savefig('result/_graph/ssim_TM1.png')
    plt.show()
    
    print('save_ssim')
    
    
    
def graph_one(output_file):
    psnr = []
    ssim = []

    with open(output_file, "r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for line in reader:
            psnr.append(float(line[2]))
            ssim.append(float(line[5]))
            # if float(line[2]>33.4):
            #     print(line[0])
            
    fig = plt.figure("psnr", figsize=(10, 20))
    n = range(len(psnr))
    psnr_fig = fig.add_subplot(211)
    psnr_fig.plot(n, psnr, label='psnr')
    ssim_fig = fig.add_subplot(212)
    ssim_fig.plot(n, ssim, label='psnr')
    plt.savefig('result/CF_TM2.png')
    plt.show()
    
    print('save_img')
    
    
    
if __name__=='__main__':
    output_file = "result/_csv/metrics_TM1.csv"
    
    graph_all(output_file)