from flask_mail import Message
from flask import current_app
from app import mail


def send_email(to_address, subject, body, attachment_path=None):
    if not current_app.config.get('MAIL_USERNAME'):
        print("=" * 50)
        print("[EMAIL — not configured, printing instead]")
        print(f"To: {to_address}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        if attachment_path:
            print(f"Attachment: {attachment_path}")
        print("=" * 50)
        return True

    msg = Message(subject=subject, recipients=[to_address], body=body)

    if attachment_path:
        with open(attachment_path, 'rb') as f:
            msg.attach(
                filename=attachment_path.split('/')[-1],
                content_type='text/csv',
                data=f.read(),
            )

    mail.send(msg)
    print(f"[EMAIL] Real email sent to {to_address}")
    return True
