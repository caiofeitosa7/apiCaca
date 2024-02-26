import base64
import os

from PIL import Image
from io import BytesIO
from datetime import datetime


def base64_to_image(str_base64):
    try:
        str_base64 = str_base64.split(';base64,')[1]
        image_data = base64.b64decode(str_base64)
        image = Image.open(BytesIO(image_data))
        nome_arquivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
        image.save(os.path.join('imagens', nome_arquivo))

        return nome_arquivo
    except Exception as e:
        print("Erro ao converter base64 para imagem:", e)
        return None


def image_to_base64(imagem):
    path_img = os.path.join('imagens', imagem)

    try:
        with open(path_img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return "data:image/jpeg;base64," + encoded_string.decode("utf-8")

    except Exception as e:
        print("Erro ao converter imagem para base64:", e)
        return None


# imgB64 = image_to_base64("20240226_151720_253363.png")
#
# with open("teste.txt", "w") as f:
#     f.write(imgB64)
#     f.close()














