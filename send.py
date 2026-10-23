import smtplib, sys
from email.message import EmailMessage

EICAR = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
mode = sys.argv[1] if len(sys.argv) > 1 else "clean"
attach = mode in ("eicar", "show")

m = EmailMessage()
m["From"], m["To"] = "alice@example.com", "bob@example.com"
m["Subject"] = "EICAR test" if attach else "Clean test"
m.set_content("Hello Bob")
if attach:
    m.add_attachment(EICAR.encode(), maintype="application",
                     subtype="octet-stream", filename="eicar.com")

if mode == "show":
    print("=== EICAR test string (harmless, industry standard fake virus) ===")
    print(EICAR)
    print()
    print("=== Full email that will be sent ===")
    print(m.as_string())
    sys.exit(0)

try:
    with smtplib.SMTP("localhost", 2525) as s:
        s.send_message(m)
    print("SENT OK")
except smtplib.SMTPDataError as e:
    print("BLOCKED:", e.smtp_code, e.smtp_error.decode())
