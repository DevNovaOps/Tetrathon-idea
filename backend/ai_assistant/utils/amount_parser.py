import re

def parse_amount(text: str) -> int | None:
    """
    Parses a string containing an Indian currency amount and returns an integer.
    Supports k, lakh, crore, commas, and rupee symbols.
    Returns None if parsing fails or if the value is negative.
    """
    if not text or not isinstance(text, str):
        return None

    # Lowercase and remove ₹, commas, and spaces
    text = text.lower().replace('₹', '').replace(',', '').replace(' ', '')
    
    # Check for negative sign
    if '-' in text:
        return None
        
    try:
        # Handle k (thousands)
        if 'k' in text:
            val = float(text.replace('k', ''))
            return int(val * 1_000)
            
        # Handle lakh (l, lac, lakh)
        if 'lakh' in text or 'lac' in text or text.endswith('l'):
            clean = text.replace('lakh', '').replace('lac', '').replace('l', '')
            val = float(clean)
            return int(val * 100_000)
            
        # Handle crore (cr, crore)
        if 'crore' in text or 'cr' in text:
            clean = text.replace('crore', '').replace('cr', '')
            val = float(clean)
            return int(val * 10_000_000)
            
        # Standard numeric
        # Extract only digits and decimal point
        numeric_part = re.sub(r'[^\d.]', '', text)
        if not numeric_part:
            return None
            
        val = float(numeric_part)
        return int(val)
        
    except ValueError:
        return None


def format_inr(amount: int) -> str:
    """Formats an integer into Indian Rupee string (e.g., 1250000 -> ₹12,50,000)."""
    if amount is None:
        return ""
        
    amount_str = str(amount)
    
    # Handle less than 1000
    if len(amount_str) <= 3:
        return f"₹{amount_str}"
        
    # Split into last 3 digits and the rest
    last_three = amount_str[-3:]
    rest = amount_str[:-3]
    
    # Chunk the rest by 2 digits from right to left
    chunks = []
    while len(rest) > 0:
        chunks.append(rest[-2:])
        rest = rest[:-2]
        
    # Reverse chunks, join with commas, and add last three
    chunks.reverse()
    formatted = ",".join(chunks) + "," + last_three
    
    return f"₹{formatted}"


def normalize_amount(text: str) -> dict | None:
    """Returns dict with numeric value and formatted string, or None if invalid."""
    value = parse_amount(text)
    if value is None or value < 0:
        return None
        
    return {
        "value": value,
        "display": format_inr(value),
        "currency": "INR"
    }
