import sys
import qrcode
import random
import string
import time
import hmac
import base64
import struct
import hashlib
import math

def process_input():
    if len(sys.argv) <= 1 or (len(sys.argv) >= 3 and sys.argv[1] != "--generate-qr" and sys.argv[1] != "--get-otp"):
        print("Invalid command. Try '--generate-qr' or '--get-otp'")
        exit()
    elif sys.argv[1] == "--generate-qr":
        generate_code()
        exit()
    elif sys.argv[1] == "--get-otp":
        get_one_time_password()
        exit()

def generate_code():
    user_email = str('test@example.com')
    issuer = str('Auth App')
    secret_key = ''.join(random.choice(string.ascii_uppercase) for i in range(32))

    with open("./secret.txt", "w") as file:
        file.write(secret_key)

    uri = f'otpauth://totp/{issuer}:{user_email}?secret={secret_key}&issuer={issuer}'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("./QR_output.jpg")

    print("QR Code successfully generated!")

def calculate_hotp(secret_key, intervals):
    key = base64.b32decode(secret_key, True)
    msg = struct.pack(">Q", intervals)
    hash_obj = hmac.new(key, msg, hashlib.sha1)
    offset = hash_obj.digest()[-1] & 0xf
    truncated_hash = struct.unpack(">I", hash_obj.digest()[offset:offset + 4])[0] & 0x7fffffff
    return truncated_hash % (10 ** 6)

def get_one_time_password():
    with open('./secret.txt', 'r') as file:
        for line in file:
            key = line.strip()

    initialsleep = 30 - (time.time()%30)
    print('Syncing with Google authenticator one moment...')
    print("Sleeping for ", math.floor(initialsleep), "Seconds")
    intervals = int(time.time()) // 30
    hotp = calculate_hotp(key, intervals)
    print("Security Code:", f"{hotp:06d}")
    time.sleep(math.floor(initialsleep))
    time.sleep(.7) #get over initial delay
    while True:
        intervals = int(time.time()) // 30
        hotp = calculate_hotp(key, intervals)
        print("Security Code:", f"{hotp:06d}")
        time.sleep(30)

def start_program():
    process_input()

if __name__ == "__main__":
    start_program()

