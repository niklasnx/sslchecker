import ssl
import socket
import smtplib
from datetime import datetime

def get_ssl_expiry(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y GMT")
                days_left = (expiry_date - datetime.utcnow()).days
                return expiry_date, days_left
    except socket.gaierror as e:
        return None, f"DNS resolution error: {e}"
    except ConnectionRefusedError as e:
        return None, f"Connection error: {e}"
    except Exception as e:
        return None, f"General error: {e}"

def load_domains(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: File domains.txt not found.")
        return []

def send_email(report, sender_email, receiver_email, smtp_server, smtp_port, smtp_user, smtp_password):
    subject = "Weekly SSL Report"
    
    html_body = """
    <html>
    <body>
        <h2>SSL Certificate Report</h2>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
            <tr>
                <th>Domain</th>
                <th>Expiration Date</th>
                <th>Days Remaining</th>
            </tr>
    """
    
    for entry in report:
        domain, expiry_date, days_left = entry
        days_style = "color: red; font-weight: bold;" if isinstance(days_left, int) and days_left < 20 else ""
        html_body += f"""
        <tr>
            <td>{domain}</td>
            <td>{expiry_date}</td>
            <td style='{days_style}'>{days_left}</td>
        </tr>
        """
    
    html_body += "</table></body></html>"
    
    message = f"Subject: {subject}\nMIME-Version: 1.0\nContent-Type: text/html\n\n{html_body}".encode("utf-8")
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_email, message)
        print("Status email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_domains(domain_list):
    report = []
    for domain in domain_list:
        expiry_date, days_left = get_ssl_expiry(domain)
        if isinstance(days_left, int):
            print(f"{domain}: SSL certificate expires on {expiry_date} ({days_left} days left)")
        else:
            print(f"{domain}: {days_left}")
        report.append((domain, expiry_date, days_left))
    return report

if __name__ == "__main__":
    domains = load_domains("domains.txt")
    if domains:
        report = check_domains(domains)
        
        sender_email = "your_email@example.com"
        receiver_email = "recipient@example.com"
        smtp_server = "your_smtp_server"
        smtp_port = 587
        smtp_user = "your_smtp_user"
        smtp_password = "your_smtp_password"
        
        send_email(report, sender_email, receiver_email, smtp_server, smtp_port, smtp_user, smtp_password)
