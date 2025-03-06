import os
import hashlib
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

# URL della pagina da monitorare
URL = 'https://www.ustli.it/usp_livorno/index.php/docenti/interpelli'

# Nome dell'istituto da monitorare
ISTITUTO_TARGET = "ITIS Galilei di Livorno"

# Configurazione Email (da GitHub Secrets)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")  
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  
EMAIL_RECEIVER = "filippo.freschi30@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# 🔹 File per salvare l'hash dell'ultimo interpello visto
HASH_FILE = "last_hash.txt"

print("🔹 Script avviato...")

def get_interpellis():
    """Scarica la pagina e recupera gli interpelli dell'ITIS Galilei di Livorno."""
    print("🔹 Scaricamento della pagina...")
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore durante il download: {e}")
        return []

    print("🔹 Pagina scaricata con successo!")
    soup = BeautifulSoup(response.text, 'html.parser')

    interpellis = []
    for item in soup.find_all('a', href=True):
        text = item.get_text(strip=True)
        link = item['href']
        if "interpello" in text.lower() and ISTITUTO_TARGET.lower() in text.lower():
            full_link = link if "http" in link else URL
            interpellis.append((text, full_link))

    print(f"🔹 Trovati {len(interpellis)} interpelli per {ISTITUTO_TARGET}")
    return interpellis

def get_page_hash(interpellis):
    """Calcola un hash basato sugli interpelli trovati."""
    return hashlib.md5("".join([i[0] for i in interpellis]).encode('utf-8')).hexdigest()

def read_last_hash():
    """Legge l'hash salvato dall'ultima esecuzione."""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_current_hash(current_hash):
    """Salva l'hash attuale per il prossimo controllo."""
    with open(HASH_FILE, "w") as f:
        f.write(current_hash)

def send_email(new_interpellis):
    """Invia un'email se ci sono nuovi interpelli."""
    if not new_interpellis:
        print("🔹 Nessun nuovo interpello, nessuna email inviata.")
        return

    print("🔹 Invio email di notifica...")
    subject = f"Nuovo interpello per {ISTITUTO_TARGET}"
    body = "Sono stati pubblicati nuovi interpelli:\n\n"

    for title, link in new_interpellis:
        body += f"- {title}\n  {link}\n\n"

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

# 🔹 Controlla la pubblicazione di nuovi interpelli
print("🔹 Controllo aggiornamenti...")
interpellis = get_interpellis()

if interpellis:
    current_hash = get_page_hash(interpellis)
    last_hash = read_last_hash()

    if current_hash != last_hash:
        print("🔹 Nuovo interpello rilevato!")
        send_email(interpellis)
        save_current_hash(current_hash)
    else:
        print("🔹 Nessun nuovo interpello, nessuna azione necessaria.")
else:
    print("❌ Nessun interpello trovato.")

print("✅ Script completato con successo!")
