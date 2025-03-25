# SSL Certificate Expiry Checker

## Overview
This script checks the SSL certificate expiration date for a list of domains and sends a formatted HTML report via email. If a certificate expires in less than 20 days, the remaining days are highlighted in red.

## Features
- Fetches SSL certificate expiration dates for domains.
- Generates an HTML email report with a table.
- Highlights certificates expiring in less than 20 days.
- Sends the report via SMTP.
- Recommended for use with a cron job to run weekly.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/niklasnx/sslchecker.git
   cd sslchecker
   ```


## Configuration
1. **Add your domains**: Edit `domains.txt` and list the domains you want to check, one per line.
2. **SMTP Settings**: Edit the file `config.py` in the project directory and add your SMTP data:
   ```python
   SMTP_CONFIG = {
       "sender_email": "your_email@example.com",
       "receiver_email": "recipient@example.com",
       "smtp_server": "your_smtp_server",
       "smtp_port": 587,
       "smtp_user": "your_smtp_user",
       "smtp_password": "your_smtp_password"
   }
   ```

## Usage
Run the script manually:
```bash
python sslchecker.py
```

### Automate with Cron
To run the script weekly, add this line to your crontab (`crontab -e`):
```cron
0 8 * * 1 /usr/bin/python3 /path/to/sslchecker.py
```
This runs the script every Monday at 8 AM.

## Security Note
Do **not** store SMTP credentials in the script. Use the `config.py` file and ensure it is excluded from version control (add it to `.gitignore`).

## License
MIT License

