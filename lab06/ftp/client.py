from ftplib import FTP

ftp = FTP('ftp.dlptest.com')
user = 'dlpuser'
pswd = 'rNrKYTX9g7z3RgJRmxWuGHbeu'
print(ftp.login(user, pswd))
while True:
    cmd = input().lower().strip()
    try:
        if cmd == 'list':
            data = ftp.retrlines('LIST')
            print(data)
        elif cmd == 'upload':
            filename = input('Filename on machine: ').strip()
            servername = input('Filename on server: ').strip()
            with open(filename, 'rb') as f:
                ftp.storbinary(f'STOR {servername}', f)
        elif cmd == 'download':
            filename = input('Filename on server: ').strip()
            localname = input('Filename on machine: ').strip()
            with open(localname, 'wb') as f:
                ftp.retrbinary(f'RETR {filename}', f.write)
        elif cmd == 'quit':
            break
        else:
            print("Incorrect")
        print("OK")
    except Exception:
        print("Error, try again")
ftp.close()