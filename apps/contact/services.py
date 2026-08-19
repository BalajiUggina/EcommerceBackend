from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)

def send_contact_email(data):
    email_sender = data.get("email")
    logger.info(f"Preparing to send contact form email from: {email_sender}")
    
    email = EmailMessage(
        subject=f"Contact Form Submission from {data['name']}",
        body=f"""
Name: {data['name']}
Email: {data['email']}
Phone: {data['phone']}

Message:
{data['message']}
""",
        from_email="ugginabalaji143@gmail.com",
        to=["ugginabalaji143@gmail.com"],
        reply_to=[email_sender],
    )

    try:
        email.send()
        logger.info(f"Email sent successfully from {email_sender}")
    except Exception as exc:
        logger.error(f"SMTP error while sending email from {email_sender}: {str(exc)}", exc_info=True)
        raise exc