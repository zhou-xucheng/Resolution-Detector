import cv2
import numpy as np


def calculate_resolution(image_path):
    # --- 从这里开始替换 ---
    try:
        # 先尝试直接读
        img = cv2.imread(image_path)
        # 如果是中文路径导致读不出来（img是None），走下面这个备用方案
        if img is None:
            img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        raise ValueError(f"读取图片出错: {e}")
    # --- 替换结束，后面代码保持原样 ---

    # 下面的代码千万别动，保持原样
    if img is None:
        raise ValueError("无法读取图片文件")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    edge_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    edge_mean = np.mean(edge_magnitude)
    edge_std = np.std(edge_magnitude)
    
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_var = np.var(laplacian)
    
    canny = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(canny > 0) / (gray.shape[0] * gray.shape[1])
    
    contrast = calculate_contrast(gray)
    
    resolution_estimate = (edge_mean * 10 + laplacian_var * 0.1 + edge_density * 500) * (contrast / 100)
    
    return resolution_estimate, contrast

def calculate_contrast(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    mean_intensity = np.mean(gray)
    max_val = np.max(gray)
    min_val = np.min(gray)
    
    if max_val == min_val:
        return 0.0
    
    rms_contrast = np.sqrt(np.mean((gray - mean_intensity) ** 2))
    drange_contrast = (max_val - min_val) / (max_val + min_val + 1e-6)
    
    contrast = (rms_contrast + drange_contrast * 255) / 2
    
    return contrast
