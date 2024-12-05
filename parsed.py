from urllib.parse import urlparse, parse_qs

URL = 'http://127.0.0.1:8050/financial_transaction_management/new_transaction?mode=edit&id=4'

# Parse the URL
parsed = urlparse(URL)

# Get the mode
create_mode = parse_qs(parsed.query).get('mode', [''])[0]

# Get the payment ID
payment_id = int(parse_qs(parsed.query).get('id', [0])[0])

print("Create Mode:", create_mode)
print("Payment ID:", payment_id)
