import smtplib
import re
from email.message import EmailMessage
from flask import Flask, request, jsonify

# -------- CONFIG --------
SENDER_EMAIL = "ys8619050@gmail.com"     # your Gmail address
APP_PASSWORD = "vjzueielbjangxom"     # your Gmail App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
# ------------------------

app = Flask(__name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def api(success, msg=None, error=None):
    return jsonify({
        "success": success,
        "message": msg,
        "error": error
    })

def send(from_name, to_email, subject, message):
    try:
        msg = EmailMessage()
        msg["From"] = f"{from_name} <{SENDER_EMAIL}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(message)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return True, "Email sent successfully!"
    
    except Exception as e:
        return False, str(e)

@app.route("/send", methods=["GET"])
def send_get():
    from_name = request.args.get("from", "")
    to_email  = request.args.get("sendto", "")
    subject   = request.args.get("subject", "")
    message   = request.args.get("message", "")

    if not validate_email(to_email):
        return api(False, error="Invalid recipient email")

    if len(message) < 5:
        return api(False, error="Message too short")

    ok, result = send(from_name, to_email, subject, message)
    return api(True, msg=result) if ok else api(False, error=result)

@app.route("/send", methods=["POST"])
def send_post():
    data = request.json or {}

    from_name = data.get("from", "")
    to_email  = data.get("sendto", "")
    subject   = data.get("subject", "")
    message   = data.get("message", "")

    if not validate_email(to_email):
        return api(False, error="Invalid recipient email")

    if len(message) < 5:
        return api(False, error="Message too short")

    ok, result = send(from_name, to_email, subject, message)
    return api(True, msg=result) if ok else api(False, error=result)

@app.route("/health")
def health():
    return api(True, msg="API is running")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)