import numpy as np
import cv2

def calculate_complexity(block):
    """
    Karmaşıklık oranını hesaplar: siyah-beyaz piksel geçişlerinin sayısını
    """
    h_transitions = np.sum(block[:, :-1] != block[:, 1:])
    v_transitions = np.sum(block[:-1, :] != block[1:, :])
    total = h_transitions + v_transitions
    max_transitions = 2 * block.shape[0] * (block.shape[1] - 1)
    return total / max_transitions

def to_bit_planes(image):
    """
    8 bit düzleme ayır
    """
    height, width = image.shape
    bit_planes = np.zeros((8, height, width), dtype=np.uint8)
    for i in range(8):
        bit_planes[i] = (image >> i) & 1
    return bit_planes

def from_bit_planes(bit_planes):
    """
    Bit düzlemlerini tekrar birleştir
    """
    image = np.zeros(bit_planes[0].shape, dtype=np.uint8)
    for i in range(8):
        image += bit_planes[i] << i
    return image

def encode_bpcs(image_path, message, output_path, threshold=0.3):
    """
    Mesajı BPCS ile gri bir görüntüye gömer
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError("Görüntü yüklenemedi.")

    bit_planes = to_bit_planes(image)
    message_bits = ''.join(format(ord(c), '08b') for c in message)
    message_index = 0

    block_size = 8
    for plane in range(7, -1, -1):  # yüksek bit düzlemleri daha karmaşıktır
        for i in range(0, image.shape[0], block_size):
            for j in range(0, image.shape[1], block_size):
                block = bit_planes[plane][i:i+block_size, j:j+block_size]
                if block.shape != (8, 8):
                    continue

                if calculate_complexity(block) >= threshold:
                    if message_index + 64 <= len(message_bits):
                        bits = np.array(list(message_bits[message_index:message_index+64]), dtype=np.uint8)
                        bit_planes[plane][i:i+8, j:j+8] = bits.reshape((8, 8))
                        message_index += 64
                    else:
                        break

            if message_index >= len(message_bits):
                break
        if message_index >= len(message_bits):
            break

    new_image = from_bit_planes(bit_planes)
    cv2.imwrite(output_path, new_image)
    return True
