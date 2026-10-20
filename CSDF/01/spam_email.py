
from email import policy
from email.parser import Parser
from email.utils import parseaddr, parsedate_to_datetime


def get_domain(address):
    """Extract the domain from an email address."""
    return address.rsplit("@", 1)[-1].lower() if "@" in address else ""


def analyze_email(filename):
    # Read and parse the email header
    with open(filename, "r", encoding="utf-8") as file:
        message = Parser(policy=policy.default).parsestr(file.read())

    print("\n===== EMAIL HEADER ANALYSIS =====")

    # Extract basic information
    sender = message.get("From", "Not available")
    recipient = message.get("To", "Not available")
    subject = message.get("Subject", "Not available")
    date = message.get("Date", "Not available")
    reply_to = message.get("Reply-To", "Not available")
    return_path = message.get("Return-Path", "Not available")

    print("Sender      :", sender)
    print("Recipient   :", recipient)
    print("Subject     :", subject)
    print("Date        :", date)
    print("Reply-To    :", reply_to)
    print("Return-Path :", return_path)

    # Validate the date if present
    if date != "Not available":
        try:
            print("Parsed Date :", parsedate_to_datetime(date))
        except (ValueError, TypeError, OverflowError):
            print("Parsed Date : Invalid date format")

    # Display the delivery route
    received_headers = message.get_all("Received", [])
    print("\n----- EMAIL ROUTE -----")

    if received_headers:
        for step, received in enumerate(received_headers, start=1):
            print(f"Hop {step}: {received}")
    else:
        print("No Received headers found.")

    # Display email authentication results
    auth_headers = message.get_all("Authentication-Results", [])
    print("\n----- AUTHENTICATION -----")

    if auth_headers:
        for result in auth_headers:
            print(result)
    else:
        print("No Authentication-Results header found.")

    # Check for suspicious indicators
    warnings = []

    sender_address = parseaddr(sender)[1]
    reply_address = parseaddr(reply_to)[1]

    if reply_address and sender_address:
        if get_domain(reply_address) != get_domain(sender_address):
            warnings.append(
                "Reply-To domain differs from the sender's domain."
            )

    auth_text = " ".join(str(result) for result in auth_headers).lower()

    for method in ("spf", "dkim", "dmarc"):
        if f"{method}=fail" in auth_text:
            warnings.append(f"{method.upper()} authentication failed.")

    print("\n----- INVESTIGATION REPORT -----")

    if warnings:
        for warning in warnings:
            print("[WARNING]", warning)
    else:
        print("No obvious warning detected by these basic checks.")

    print("\nNote: Header analysis alone cannot prove whether an email")
    print("is genuine or fraudulent.")


if __name__ == "__main__":
    try:
        analyze_email("email_header.txt")
    except FileNotFoundError:
        print("Error: email_header.txt not found.")
        print("Create the file and paste an email header into it.")
    except (OSError, ValueError) as error:
        print("Error while analyzing the email:", error)
