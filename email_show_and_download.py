import imaplib
import email
import os
from email.header import decode_header

# Email and password (use app password if using Gmail)
EMAIL_USER = "jovaniasfaw@gmail.com"
EMAIL_PASS = "amuy vhjf zjsb qgxm"

# Create a directory to store the attachments
ATTACHMENT_DIR = "attachments"
if not os.path.exists(ATTACHMENT_DIR):
    os.makedirs(ATTACHMENT_DIR)

def clean(text):
    # Clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def download_attachments(msg):
    for part in msg.walk():
        # Check if this part has an attachment
        content_disposition = part.get("Content-Disposition", "")
        if "attachment" in content_disposition:
            # Get the attachment filename
            filename = part.get_filename()

            if filename:
                # Decode filename if it's encoded
                filename, encoding = decode_header(filename)[0]
                if isinstance(filename, bytes):
                    filename = filename.decode(encoding if encoding else "utf-8")
                
                # Clean the filename for saving
                filepath = os.path.join(ATTACHMENT_DIR, clean(filename))

                # Write the attachment to the file
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))  # Decode the payload
                print(f"Downloaded: {filename}")
            else:
                print("No filename found for the attachment.")

def check_email():
    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("jovaniasfaw@gmail.com", "amuy vhjf zjsb qgxm")
    
    # Select the mailbox you want to check
    mail.select("inbox")

    # Search for all emails
    status, messages = mail.search(None, 'ALL')

    # Convert the message IDs to a list
    email_ids = messages[0].split()
    
    # Process the most recent 5 emails
    for email_id in email_ids[-10:]:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                print(f"Subject: {subject}")

                # Print sender
                from_ = msg.get("From")
                print(f"From: {from_}")

                # Download attachments
                download_attachments(msg)

    mail.logout()

if __name__ == "__main__":
    check_email()
