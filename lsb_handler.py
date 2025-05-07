from PIL import Image

def encode_lsb(image_path, message, output_path):
    image = Image.open(image_path)
    encoded = image.copy()
    width, height = image.size
    message += chr(0)  # Bitiş karakteri (NULL)
    binary_message = ''.join([format(ord(char), '08b') for char in message])

    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index >= len(binary_message):
                break

            pixel = list(image.getpixel((x, y)))
            for i in range(3):  # R, G, B
                if data_index < len(binary_message):
                    pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
        if data_index >= len(binary_message):
            break

    encoded.save(output_path)
    return True

def decode_lsb(image_path):
    image = Image.open(image_path)
    width, height = image.size

    binary_data = ""
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    # 8 bitlik parçalara ayır ve ASCII'ye çevir
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for char in chars:
        if chr(int(char, 2)) == chr(0):
            break
        message += chr(int(char, 2))
    return message
