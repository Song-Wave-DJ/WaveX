import qrcode


def generate(Link):
    qr = qrcode.QRCode(
        version=1,  # QR code version (1 to 40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each "box" in the QR code
        border=4,  # Border width
    )

    # Add data to the QR code
    data = Link
    qr.add_data(data)

    # Make the QR code
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    # Save the image to a file
    img.save("Qr.png")
