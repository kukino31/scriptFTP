import os
import zipfile
import ftplib
import smtplib
from datetime import datetime

# Obtener la fecha actual en el formato requerido
fecha = datetime.now().strftime("%Y%m%d")

# Comprimir el directorio public_html en un archivo .zip
with zipfile.ZipFile("backup"+fecha+".zip", "w") as backup:
    for root, dirs, files in os.walk("public_html"):
        for file in files:
            backup.write(os.path.join(root, file))

# Conectarse al servidor FTP remoto
ftp = ftplib.FTP("ftp.example.com")
ftp.login("username", "password")

# Subir el archivo de copia de seguridad al servidor FTP
with open("backup"+fecha+".zip", "rb") as backup:
    ftp.storbinary("STOR backup"+fecha+".zip", backup)

# Eliminar el archivo de copia de seguridad local
os.remove("backup"+fecha+".zip")

# Cerrar la conexión FTP
ftp.quit()

# Verificar el número de copias de seguridad almacenadas en el servidor FTP
ftp.login("username", "password")
ftp.cwd("/")
backups = ftp.nlst()
backups_count = len([b for b in backups if "backup" in b])

# Eliminar la copia de seguridad más antigua si hay más de 10
if backups_count > 10:
    oldest_backup = sorted(backups)[0]
    ftp.delete(oldest_backup)

# Cerrar la conexión FTP
ftp.quit()

# Enviar un correo electrónico de confirmación
server = smtplib.SMTP("smtp.example.com")
server.login("username", "password")
msg = "La copia de seguridad del directorio public_html se ha completado con éxito."
server.sendmail("sender@example.com", "admin@example.com", msg)
server.quit()
