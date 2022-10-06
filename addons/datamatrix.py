from pylibdmtx.pylibdmtx import encode, decode
from PIL import Image

def make_datamatrix(data, name="datamatrix.png"):
    encoded = encode(data.encode("utf8"))
    img = Image.frombytes("RGB", (encoded.width, encoded.height), encoded.pixels)
    img.save(name)

    return name
