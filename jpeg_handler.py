import numpy as np
import cv2
from scipy.fftpack import dct, idct

def encode_jpeg_dct(image_path, message, output_path):
    # Görüntüyü oku
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Görüntü yüklenemedi.")
    
    # Görüntüyü gri tonlamaya çevir
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Mesajı bitlere dönüştür
    message += chr(0)  # Bitiş karakteri
    binary_message = ''.join([format(ord(char), '08b') for char in message])

    # Görüntüyü 8x8 bloklara ayır
    height, width = gray_image.shape
    block_size = 8
    encoded_image = gray_image.copy()

    data_index = 0
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = gray_image[i:i+block_size, j:j+block_size]

            # DCT dönüşümünü yap
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')

            # Mesajı DCT'nin düşük frekans bileşenlerine yerleştir
            if data_index < len(binary_message):
                bit = int(binary_message[data_index])
                # DCT'nin düşük frekans bileşenini tam sayıya çevirip bitwise işlemi yap
                dct_block[0, 0] = int(dct_block[0, 0]) & ~1 | bit
                data_index += 1

            # Ters DCT dönüşümünü yaparak bloğu geri al
            encoded_image[i:i+block_size, j:j+block_size] = np.round(idct(idct(dct_block.T, norm='ortho').T, norm='ortho'))

            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    # Encode edilmiş görüntüyü kaydet
    cv2.imwrite(output_path, encoded_image)
    return True


def decode_jpeg_dct(file_path):
    # Görüntüyü oku
    encoded_image = cv2.imread(file_path)
    
    if encoded_image is None:
        raise FileNotFoundError(f"Resim dosyası bulunamadı: {file_path}")

    print(f"Görüntü okundu, boyutlar: {encoded_image.shape}")
    
    # Görüntüyü gri tonlara dönüştür
    gray_image = cv2.cvtColor(encoded_image, cv2.COLOR_BGR2GRAY)
    
    height, width = gray_image.shape
    block_size = 8
    decoded_message = []
    
    # Düşük frekans bileşenlerine bakarak mesajı çıkar
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = gray_image[i:i+block_size, j:j+block_size]
            
            # DCT dönüşümünü yap
            dct_block = cv2.dct(np.float32(block))
            
            # İlk frekans bileşeninden (düşük frekans) mesaj bitini çıkar
            bit = int(dct_block[0, 0]) & 1
            decoded_message.append(str(bit))
    
    # Mesajı bit dizisinden metne dönüştür
    decoded_bits = ''.join(decoded_message)
    decoded_chars = [chr(int(decoded_bits[i:i+8], 2)) for i in range(0, len(decoded_bits), 8)]
    
    # Mesajın sonuna eklenen null byte'ı çıkar
    return ''.join(decoded_chars).rstrip(chr(0))