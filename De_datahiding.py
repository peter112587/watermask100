import cv2
import numpy as np

# 讀取機密影像1和機密影像2
secret_img_1 = cv2.imread('F16_block.png', cv2.IMREAD_GRAYSCALE)
secret_img_2 = cv2.imread('F16_block.png', cv2.IMREAD_GRAYSCALE)
# 讀取蓋子影像
cover_img = cv2.imread('pics/1.png', cv2.IMREAD_GRAYSCALE)

# 確認影像大小相符
assert secret_img_1.shape == secret_img_2.shape == (64, 64)
assert cover_img.shape == (256, 512)

# 將機密影像1和機密影像2轉換成二進位字符串
secret_bits_1 = ''.join(format(pixel, '08b') for pixel in secret_img_1.flatten())
secret_bits_2 = ''.join(format(pixel, '08b') for pixel in secret_img_2.flatten())

# 將蓋子影像轉換成二進位字符串
cover_bits = ''.join(format(pixel, '08b') for pixel in cover_img.flatten())

# 檢查是否有足夠的蓋子像素可以藏入機密影像
assert len(secret_bits_1) + len(secret_bits_2) <= len(cover_bits), "Cover image too small"

# 將機密影像的二進位字符串藏入蓋子影像的像素中
stego_bits = ''
cover_idx = 0
for bit_1, bit_2 in zip(secret_bits_1, secret_bits_2):
    # 將機密影像的每個像素的兩個二進位位元分別嵌入到蓋子影像的四個像素中
    cover_byte = format(cover_img.flatten()[cover_idx], '08b')
    stego_byte = cover_byte[:6] + bit_1 + cover_byte[6:7] + bit_2 + cover_byte[7:]
    stego_bits += stego_byte
    cover_idx += 1
    # 若已嵌入滿足夠的像素，則停止
    if len(stego_bits) == len(secret_bits_1) + len(secret_bits_2):
        break

# 將剩下的蓋子影像二進位位元嵌入到stego_bits中
stego_bits += cover_bits[cover_idx:]

# 將stego_bits轉換成像素值並重塑成與蓋子影像相同的形狀
stego_pixels = np.array([int(stego_bits[i:i+8], 2) for i in range(0, len(stego_bits), 8)])
stego_img = stego_pixels.reshape(cover_img.shape)

# 儲存stego影像
cv2.imwrite('DE_image.png', stego_img)