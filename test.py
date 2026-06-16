import smtplib

server = smtplib.SMTP_SSL(
    "smtp.gmail.com",
    465
)

server.login(
    "ugginabalaji2003@gmail.com",
    "sbkfevdthfetwjri"
)

print("Success")