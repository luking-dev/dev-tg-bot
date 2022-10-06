import qrcode

def make_qr(data, name="qrcode.png", version=1, box_size=8, border=2, fit=True, fill_color="black", back_color="white"):
    qr = qrcode.QRCode(version=version,
                       box_size=box_size,
                       border=border)

    qr.add_data(data)
    qr.make(fit=fit)

    img = qr.make_image(fill_color=fill_color,
                        back_color=back_color)
    img.save(name)

    return name
