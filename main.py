import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import subprocess
from datetime import datetime as dt
from time import sleep

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the MIME message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add the body to the email
        msg.attach(MIMEText(body, 'plain'))
        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")

def ping_host(host):
    try:
        # Perform a ping command
        response = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response.returncode == 0
    except Exception as e:
        print(f"Error while pinging host: {e}")
        return False

# Example usage:
if __name__ == "__main__":
    print("Starting script...")
    # Set up environment variables for sensitive information
    sender_email = os.getenv("SENDER")
    sender_password = os.getenv("PASS")
    recipient_email = "aleonard@gazellesports.com"

    if not sender_email or not sender_password:
        print("Error: Missing email credentials. Ensure SENDER and PASS are set.")
    else:
        print("Email credentials loaded successfully.")

    # Host to ping
    host_to_ping = "10.0.0.4"
    print(f"Host to ping: {host_to_ping}")

    # Check if the host is reachable
    start = dt.now()
    while True:
        if ping_host(host_to_ping):
            sleep(60)
        else:
            break

    end = dt.now()
    duration = end - start
    print(f"Ping to {host_to_ping} failed. Sending email notification.")
    subject = f"Ping Failure Alert: {host_to_ping}"
    body = f"The host {host_to_ping} is unreachable. It was up for {duration}"
    send_email(sender_email, sender_password, recipient_email, subject, body)
