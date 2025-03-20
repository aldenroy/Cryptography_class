import sys
import qrcode
import random
import string
import time
import hmac
import base64
import struct
import hashlib

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

    while True:
        intervals = int(time.time()) // 30
        hotp = calculate_hotp(key, intervals)
        print("Security Code:", f"{hotp:06d}")
        time.sleep(30)

def start_program():
    process_input()

if __name__ == "__main__":
    start_program()


# import hmac
# import base64
# import struct
# import hashlib
# import time
# import qrcode
# import sys
# import math

# DIGITS_POWER = [10 ** i for i in range(8, -1, -1)]


# def get_hotp(secret, intervals):
#     key = base64.b32decode(secret, True)
#     msg = struct.pack(">Q", intervals)
#     hash_obj = hmac.new(key, msg, hashlib.sha1)
    
#     offset = hash_obj.digest()[-1] & 0xf
#     truncated_hash = struct.unpack(">I", hash_obj.digest()[offset:offset + 4])[0] & 0x7fffffff
    
#     return truncated_hash % DIGITS_POWER[6]


# def get_totp(secret):
#     # Add padding if needed
#     while len(secret) % 8 != 0:
#         secret += '='

#     hotp = get_hotp(secret, math.floor(int(time.time()) / 30))
#     return f"{hotp:06d}"



# def generate_qr_code(secret, user_name='example@google.com', issuer_name='Secure App'):
#     start = 'otpauth://totp/'
#     mid = f'{issuer_name}%3A{user_name}?'
#     end = f'&issuer={issuer_name}'
    
#     uri = start + mid + 'secret=' + secret + end
#     qr = qrcode.QRCode(
#         version=1,
#         box_size=3,
#         border=5
#     )
#     qr.add_data(uri)
#     qr.make(fit=True)
#     code = qr.make_image(fill='black', back_color='white')
#     code.save('QRcode.jpg')
#     print("QR code generation complete.")
#     print("File created... QRcode.jpg")


# def main():
#     if len(sys.argv) != 2:
#         print("Invalid number of arguments.")
#         print("Try: --generate-qr or --get-otp ")
#         return

#     arg = sys.argv[1]

#     if arg == "--generate-qr":
#         secret = "secretmessage"
#         generate_qr_code(secret)

#     elif arg == "--get-otp":
#         initial_sleep = 30 - (time.time() % 30)
#         print('Syncing with Google authenticator one moment...')
#         print(f"Sleeping for {math.floor(initial_sleep)} Seconds")
#         time.sleep(math.floor(initial_sleep))

#         while True:
#             secret = "secretmessage"
#             print(get_totp(secret))
#             time.sleep(30)

#     else:
#         print("Invalid argument:", arg)
#         print("Try: --generate-qr or --get-otp ")


# if __name__ == "__main__":
#     main()
