import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_rmse(img1, img2):
    """Root Mean Squared Error 계산"""
    return np.sqrt(np.mean((img1 - img2) ** 2))

def calculate_psnr(img1, img2):
    """Peak Signal-to-Noise Ratio 계산"""
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')  # 완벽히 동일할 경우 PSNR은 무한대
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse))

def calculate_ssim(img1, img2):
    """Structural Similarity Index 계산"""
    # 이미지 크기에 맞는 win_size 설정, 이미지 크기보다 작은 값으로 설정
    win_size = min(img1.shape[:2])  # 이미지의 크기에 맞게 win_size 설정
    win_size = min(win_size, 7)  # 최대 7x7 크기로 제한 (이미지 크기가 너무 작을 경우)
    
    # win_size가 홀수여야 하므로, 홀수로 맞추기
    if win_size % 2 == 0:
        win_size -= 1

    # SSIM 계산 (multichannel=True일 때 channel_axis 설정)
    if img1.ndim == 3:  # 컬러 이미지일 경우
        return ssim(img1, img2, data_range=img2.max() - img2.min(), multichannel=True, win_size=win_size, channel_axis=2)
    else:  # 흑백 이미지일 경우
        return ssim(img1, img2, data_range=img2.max() - img2.min(), win_size=win_size)

def compare_images(img1_path, img2_path):
    # 이미지 불러오기
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # 이미지 크기가 다를 경우 처리
    if img1.shape != img2.shape:
        raise ValueError("이미지 크기가 서로 다릅니다.")

    # RMSE, PSNR, SSIM 계산
    rmse_value = calculate_rmse(img1, img2)
    psnr_value = calculate_psnr(img1, img2)
    ssim_value = calculate_ssim(img1, img2)

    # 결과 출력
    print(f"RMSE: {rmse_value:.4f}")
    print(f"PSNR: {psnr_value:.2f} dB")
    print(f"SSIM: {ssim_value:.4f}")

# 사용 예시
compare_images("pattern_out/pattern_5.png", "output_highres_image.jpg")
