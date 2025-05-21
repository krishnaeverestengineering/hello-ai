import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from agents import function_tool
import requests
from dotenv import load_dotenv
import urllib3
import json

load_dotenv(override=True)

@function_tool
def send_email(body: str):
    """Send an email using SendGrid.

    Args:
        body (str): The email body content
    """
    # Disable SSL verification warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        print("Error: SENDGRID_API_KEY not found in environment variables")
        return False

    from_email = Email("krishnamurthy.t@everest.engineering")  # Change to your verified sender
    to_email = To("krish.arjun009@gmail.com")  # Change to your recipient
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        # Send an HTTP POST request to /mail/send
        response = requests.post(
            'https://api.sendgrid.com/v3/mail/send',
            headers=headers,
            json=mail_json,
            verify=False  # Disable SSL verification
        )
        print(f"Email sent successfully! Status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
