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

# Configurazione Email
EMAIL_SENDER = "tuo.email@gmail.com"  # Sostituisci con il tuo indirizzo email
EMAIL_PASSWORD = "tua_password_per_app"  # Usa una password per app se usi Gmail
EMAIL_RECEIVER = "filippo.freschi30@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

print("🔹 Script avviato...")

# Funzione per ottenere gli interpelli con link
def get_interpellis():
    print("🔹 Scaricamento della pagina...")
    try:
        response = requests.get(url, timeout=15)  # Timeout di 15 secondi
        response.raise_for_status()  # Genera errore se il sito non risponde
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore durante il download: {e}")
        return []

    print("🔹 Pagina scaricata con successo!")
    soup = BeautifulSoup(response.text, 'html.parser')

    interpellis = []
    for item in soup.find_all('a', href=True):
        text = item.get_text(strip=True)
        link = item['href']
        if "interpello" in text.lower() and istituto_target.lower() in text.lower():
            interpellis.append((text, link))

    print(f"🔹 Trovati {len(interpellis)} interpelli")
    return interpellis

# Funzione per calcolare l'hash degli interpelli
def get_page_hash():
    interpellis = get_interpellis()
    return hashlib.md5("".join([i[0] for i in interpellis]).encode('utf-8')).hexdigest()

# Funzione per inviare una email di notifica
def send_email(new_interpellis):
    if not new_interpellis:
        print("🔹 Nessun interpello trovato, nessuna email inviata.")
        return
    
    print("🔹 Invio email di notifica...")
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
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("✅ Email inviata con successo!")
    except Exception as e:
        print(f"❌ Errore nell'invio dell'email: {e}")

# Esegue un solo controllo e termina
print("🔹 Controllo aggiornamenti...")
interpellis = get_interpellis()
send_email(interpellis)

print("✅ Script completato con successo!")
