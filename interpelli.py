import smtplib
from email.mime.text import MIMEText

# Configura l'email
SENDER_EMAIL = os.getenv("EMAIL_SENDER")  # 🔹 Usa il tuo indirizzo Gmail
RECEIVER_EMAIL = "filippo.freschi30@gmail.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")  # 🔹 Usa la password per app di Google

def get_interpellis():
    """Simula l'estrazione degli interpelli dal sito."""
    return [
        ("Interpello 1", "https://www.ustli.it/interpello1"),
        ("Interpello 2", "https://www.ustli.it/interpello2"),
    ]

def send_email(subject, body):
    """Invia un'email con il nuovo interpello trovato."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"✅ Email inviata con successo: {subject}")
    except Exception as e:
        print(f"❌ Errore nell'invio email: {e}")

# 🔹 Aggiungiamo un interpello finto per test
test_interpello = [("Finto Interpello - TEST", "https://www.ustli.it/test-link")]

# 🔹 Recuperiamo gli interpelli reali e uniamo il test
interpellis = test_interpello + get_interpellis()

# 🔹 Invia un'email per ogni interpello trovato
for title, link in interpellis:
    subject = f"Nuovo interpello: {title}"
    body = f"È stato pubblicato un nuovo interpello:\n{title}\nLink: {link}"
    send_email(subject, body)  # ✅ Adesso passiamo i due parametri correttamente!


interpellis = get_interpellis()
send_email(interpellis)

print("✅ Script completato con successo!")
