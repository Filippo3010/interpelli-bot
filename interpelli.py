import smtplib
from email.mime.text import MIMEText

def get_interpellis():
    """Simula l'estrazione degli interpelli dal sito."""
    return [
        ("Interpello 1", "https://www.ustli.it/interpello1"),
        ("Interpello 2", "https://www.ustli.it/interpello2"),
    ]

def send_email(subject, body):
    """Invia un'email con il nuovo interpello trovato."""
    sender_email = "tuoemail@gmail.com"
    receiver_email = "filippo.freschi30@gmail.com"
    password = "TUA_PASSWORD"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email inviata con successo!")
    except Exception as e:
        print(f"❌ Errore nell'invio email: {e}")

# ✅ Aggiungiamo un interpello finto per testare la notifica
test_interpello = [("Finto Interpello - TEST", "https://www.ustli.it/test-link")]

# 📌 Uniamo il test con gli interpelli veri
interpellis = test_interpello + get_interpellis()

# 📩 Invia email per ogni interpello trovato
for title, link in interpellis:
    subject = f"Nuovo interpello: {title}"
    body = f"È stato pubblicato un nuovo interpello:\n{title}\nLink: {link}"
    send_email(subject, body)

interpellis = get_interpellis()
send_email(interpellis)

print("✅ Script completato con successo!")
