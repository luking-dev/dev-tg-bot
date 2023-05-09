from barcode import *
from barcode.writer import ImageWriter
  
def make_barcode(data, name="barcode"):
    barcode_format = get_barcode_class("ean13")
    barcode = barcode_format(data, writer=ImageWriter())

    return barcode.save(name)
    