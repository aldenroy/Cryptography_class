First you need to make sure qrcode is installed.
Run: pip install qrcode
to get that module. 
Based off running this on this server this should be everything
you need to install.

Then open google authenticator on your phone to get it ready.
Run: python3 totp.py --generate-qr
This will generate a qrcode called QR_output.jpg
The qr code does work, it's how I've been testing it on vscode.
Make sure to use google authenticator qr code scanner in the app like the main
assignment says to. I tried using normal camera and that won't work cause it thinks it's a normal password and tries to add it to password manager.

Open that qrcode code file and use the scan a qrcode in google authenticator. 
This will generate a OTP that refreshes every 30 seconds.
 
Next run: python3 totp.py --get-otp
This will display the OTP in the terminal and it will match with the
one on your phone. They will always end up being the same within 30 
seconds. Depending on when in the timer you run --get-otp, the
code in google authenticator may switch earlier, and then you just have 
to wait less than 30 seconds for the terminl to sync up.

Run ctrl-c at any point to finish running, or it will give you code forever.