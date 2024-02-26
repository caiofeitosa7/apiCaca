from io import BytesIO
from PIL import Image
import base64

with open('agenda-medica.webp', 'rb') as image_file:
    # base64_bytes = base64.b64encode(image_file.read())
    base64_bytes = base64.b64encode()
    print(base64_bytes)

    base64_string = base64_bytes.decode()
    print(base64_string)

    im = Image.open(BytesIO(base64.b64decode(base64_bytes)))
    im.save('house2.png', 'PNG')
