# python lab.py --GT_dir=(GT 이미지 위치) --data_dir=(colorization한 이미지 위치) --save_dir=(csv 파일 저장 위치)

import os, sys, csv, cv2, math, argparse
sys.path.append("/mnt/e/Program/Python/Colorization")
import numpy as np
from scipy.linalg import sqrtm



def argparser(parser):
    parser.add_argument('--GT_dir', default='dataset/TM2/Color', type=str, help='GT dir')
    parser.add_argument('--data_dir', default='result/TM1', type=str, help='Colorization dir')
    parser.add_argument('--save_dir', default='result/_csv/metrics_TM1.csv', type=str, help='save dir')
    return parser



def psnr(img_1, img_2):
    mse = np.square(np.subtract(img_1, img_2)).mean()
    psnr = math.log10((255**2)/mse) * 10.
    return psnr



def ssim(img_1, img_2):
    C_1 = (0.01 * 255)**2
    C_2 = (0.03 * 255)**2
    
    img_1 = img_1.astype(np.float64)
    img_2 = img_2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu_1 = cv2.filter2D(img_1, -1, window)[5:-5, 5:-5]  # valid
    mu_2 = cv2.filter2D(img_2, -1, window)[5:-5, 5:-5]
    mu_sq_1 = mu_1**2
    mu_sq_2 = mu_2**2
    mu1_mu2 = mu_1 * mu_2
    sigma_sq_1 = cv2.filter2D(img_1**2, -1, window)[5:-5, 5:-5] - mu_sq_1
    sigma_sq_2 = cv2.filter2D(img_2**2, -1, window)[5:-5, 5:-5] - mu_sq_2
    sigma = cv2.filter2D(img_1 * img_2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C_1) * (2 * sigma + C_2)) / ((mu_sq_1 + mu_sq_1 + C_1) *(sigma_sq_1 + sigma_sq_2 + C_2))
    return ssim_map.mean()



def fid(img_1, img_2):
    mu_1, sigma_1 = img_1.mean(axis=0), np.cov(img_1, rowvar=False)
    mu_2, sigma_2 = img_2.mean(axis=0), np.cov(img_2,  rowvar=False)
    
    ssdiff = np.sum((mu_1 - mu_2)**2.0)
    
    covmean = sqrtm(sigma_1.dot(sigma_2))
    if np.iscomplexobj(covmean):
       covmean = covmean.Real
    fid = ssdiff + np.trace(sigma_1 + sigma_2 - 2.0 * covmean)
    return fid



def cal_metrics_one(imgs_dir_1, imgs_dir_2, save_dir):
    img_list_1 = sorted(os.listdir(imgs_dir_1))
    img_list_2 = sorted(os.listdir(imgs_dir_2))
    fid_list = []
    psnr_list = []
    ssim_list = []
    
    total_imgs = len(img_list_2)
    progress = 1
    
    save_name = 'metrics_CF_TM2.csv'
    header = ['img_1', 'img_2', 
              'psnr', 'psnr_a', 'psnr_b',
              'ssim', 'ssim_a', 'ssim_b']
    
    save_file = os.path.join(save_dir, save_name)
    
    with open(save_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        
        for img_dir_2 in img_list_2:
            img_1 = cv2.imread(os.path.join(imgs_dir_1, img_dir_2[:-5]+'4.png'), cv2.IMREAD_COLOR)
            img_1 = cv2.resize(img_1, (256, 256), interpolation=cv2.INTER_CUBIC)
            img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2LAB)
            img_2 = cv2.imread(os.path.join(imgs_dir_2, img_dir_2), cv2.IMREAD_COLOR)
            img_2 = cv2.resize(img_2,(256, 256), interpolation=cv2.INTER_CUBIC)
            img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2LAB)
            
            a_1 = img_1[:,:,1]+128.
            b_1 = img_1[:,:,2]+128.
            a_2 = img_2[:,:,1]+128.
            b_2 = img_2[:,:,2]+128.
            
            psnr_a = psnr(a_1, a_2)
            psnr_b = psnr(b_1, b_2)
            ssim_a = ssim(a_1, a_2)
            ssim_b = ssim(b_1, b_2)
            
            writer.writerow([img_dir_2, img_dir_2.split('/')[-1], 
                             (psnr_a+psnr_b)/2, psnr_a, psnr_b, 
                             (ssim_a+ssim_b)/2, ssim_a, ssim_b])
            
            psnr_list.append((psnr_a+psnr_b)/2)
            ssim_list.append((ssim_a+ssim_b)/2)
            
            print(f'{progress}/{total_imgs}')
            progress +=1
            
    print('psnr 평균:', np.mean(psnr_list))
    print('ssim 평균:', np.mean(ssim_list))
    
    print(f"save")
    
    

def cal_metrics_all(GTs_dir: str, imgs_dir: str, save_dir: str):
    GT_list = sorted(os.listdir(GTs_dir))
    cGAN_list = sorted(os.listdir(os.path.join(imgs_dir, 'cGAN')))
    CF_list = sorted(os.listdir(os.path.join(imgs_dir, 'ColorFormer')))
    DISCO_list = sorted(os.listdir(os.path.join(imgs_dir, 'DISCO')))
    UGATIT_list = sorted(os.listdir(os.path.join(imgs_dir, 'UGATIT')))
    
    header = ['name', 
              'cGAN_psnr', 'cGAN_ssim', 
              'CF_psnr', 'CF_ssim', 
              'DISCO_psnr', 'DISCO_ssim', 
              'UGATIT_psnr', 'UGATIT_ssim']

    save_file = save_dir

    metrics_list = []
    progress = 1
    total_imgs = len(GT_list)

    print('start')
    with open(save_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for GT_dir, cGAN_dir, CF_dir, DISCO_dir, UGATIT_dir in zip(GT_list, cGAN_list, CF_list, DISCO_list, UGATIT_list):
            img_GT = cv2.cvtColor(cv2.resize(cv2.imread(os.path.join(GTs_dir, GT_dir), cv2.IMREAD_COLOR),(256, 256), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2LAB)
            img_cGAN = cv2.cvtColor(cv2.resize(cv2.imread(os.path.join(imgs_dir, 'cGAN', cGAN_dir), cv2.IMREAD_COLOR),(256, 256), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2LAB)
            img_CF = cv2.cvtColor(cv2.resize(cv2.imread(os.path.join(imgs_dir, 'ColorFormer', CF_dir), cv2.IMREAD_COLOR),(256, 256), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2LAB)
            img_DISCO = cv2.cvtColor(cv2.resize(cv2.imread(os.path.join(imgs_dir, 'DISCO', DISCO_dir), cv2.IMREAD_COLOR),(256, 256), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2LAB)
            img_UGATIT = cv2.cvtColor(cv2.resize(cv2.imread(os.path.join(imgs_dir, 'UGATIT', UGATIT_dir), cv2.IMREAD_COLOR),(256, 256), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2LAB)

            a_GT = img_GT[:,:,1]+128.
            a_cGAN = img_cGAN[:,:,1]+128.
            a_CF = img_CF[:,:,1]+128.
            a_DISCO = img_DISCO[:,:,1]+128.
            a_UGATIT = img_UGATIT[:,:,1]+128.

            b_GT = img_GT[:,:,2]+128.
            b_cGAN = img_cGAN[:,:,2]+128.
            b_CF = img_CF[:,:,2]+128.
            b_DISCO = img_DISCO[:,:,2]+128.
            b_UGATIT = img_UGATIT[:,:,2]+128.

            metrics = [GT_dir, 
                       (psnr(a_GT, a_cGAN)+psnr(b_GT, b_cGAN))/2, (ssim(a_GT, a_cGAN)+ssim(b_GT, b_cGAN))/2,
                       (psnr(a_GT, a_CF)+psnr(b_GT, b_CF))/2, (ssim(a_GT, a_CF)+ssim(b_GT, b_CF))/2,
                       (psnr(a_GT, a_DISCO)+psnr(b_GT, b_DISCO))/2, (ssim(a_GT, a_DISCO)+ssim(b_GT, b_DISCO))/2,
                       (psnr(a_GT, a_UGATIT)+psnr(b_GT, b_UGATIT))/2, (ssim(a_GT, a_UGATIT)+ssim(b_GT, b_UGATIT))/2]

            writer.writerow(metrics)
            metrics_list.append(metrics)
            print(f'{progress}/{total_imgs}')
            progress +=1


    print('---cGAN---')
    cGAN_psnr = [item[1] for item in metrics]
    print('psnr 평균:', np.mean(cGAN_psnr))
    cGAN_ssim = [item[2] for item in metrics]
    print('ssim 평균:', np.mean(cGAN_ssim))
    print('---CF---')
    CF_psnr = [item[3] for item in metrics]
    print('psnr 평균:', np.mean(CF_psnr))
    CF_ssim = [item[4] for item in metrics]
    print('ssim 평균:', np.mean(CF_ssim))
    print('---cGAN---')
    DISCO_psnr = [item[5] for item in metrics]
    print('psnr 평균:', np.mean(DISCO_psnr))
    DISCO_ssim = [item[6] for item in metrics]
    print('ssim 평균:', np.mean(DISCO_ssim))
    print('---cGAN---')
    UGATIT_psnr = [item[7] for item in metrics]
    print('psnr 평균:', np.mean(UGATIT_psnr))
    UGATIT_ssim = [item[8] for item in metrics]
    print('ssim 평균:', np.mean(UGATIT_ssim))



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser = argparser(parser)
    args = parser.parse_args()
    
    cal_metrics_all(args.GT_dir, args.data_dir, args.save_dir)