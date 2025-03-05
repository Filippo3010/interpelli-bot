import time
import hashlib
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

# URL della pagina da monitorare
url = 'https://www.ustli.it/usp_livorno/index.php/docenti/interpelli'

# Nome dell'istituto da monitorare
istituto_target = "ITIS Galilei di Livorno"

# Configurazione Email (sarà gestita con GitHub Secrets)
EMAIL_SENDER = "il_tuo_indirizzo_email"
EMAIL_RECEIVER = "filippo.freschi30@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Funzione per ottenere gli interpelli con link
def get_interpellis():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    interpellis = []
    for item in soup.find_all('a', href=True):  # Prende solo i link
        text = item.get_text(strip=True)
        link = item['href']
        if "interpello" in text.lower() and istituto_target.lower() in text.lower():
            interpellis.append((text, link))

    return interpellis

# Funzione per calcolare l'hash degli interpelli
def get_page_hash():
    interpellis = get_interpellis()
    return hashlib.md5("".join([i[0] for i in interpellis]).encode('utf-8')).hexdigest()

# Funzione per inviare una email di notifica
def send_email(new_interpellis):
    subject = f"Nuovo interpello per {istituto_target}"

    body = "Sono stati pubblicati nuovi interpelli:\n\n"
    for title, link in new_interpellis:
        full_link = url if "http" not in link else link  # Corregge link relativi
        body += f"- {title}\n  {full_link}\n\n"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

# Ottieni l'hash iniziale della pagina
previous_hash = get_page_hash()

# Monitora la pagina a intervalli regolari
while True:
    time.sleep(300)  # Controlla ogni 5 minuti
    current_hash = get_page_hash()

    if current_hash != previous_hash:
        interpellis = get_interpellis()



        if interpellis:
            send_email(interpellis)

        previous_hash = current_hash
        # Modifica di test per attivare il workflow

