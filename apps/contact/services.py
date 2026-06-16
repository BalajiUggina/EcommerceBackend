from django.core.mail import EmailMessage

def send_contact_email(data):
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
        reply_to=[data["email"]],
    )

    email.send()