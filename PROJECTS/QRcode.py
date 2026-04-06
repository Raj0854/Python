#creating a qrcode
import qrcode
QR=qrcode.make("https://github.com/Raj0854")
QR.save("github.png")
print("qr generated successfully")