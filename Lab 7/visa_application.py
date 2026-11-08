def parse_application(text):
    """
    Parses visa type and number of entries from a colon-separated string.
    Expected format: "visa_type:entries" (e.g. "tourist:2")
    Returns: (visa_type, entries) as (str, int) or (None, None) if invalid/empty.
    """
    if not text or not isinstance(text, str):
        return None, None

    parts = text.split(':')
    if len(parts) != 2:
        return None, None

    visa, entries = parts
    visa = visa.strip()
    entries = entries.strip()

    if not visa:
        return None, None

    try:
        entries_count = int(entries)
        if entries_count < 0:
            return None, None
        return visa.title(), entries_count
    except (ValueError, TypeError):
        return None, None


def processing_average(days_csv):
    """
    Averages processing days given as comma-separated values.
    Expected format: "5,10,21"
    Returns: integer average of valid processing days, or 0 if none.
    """
    if not days_csv or not isinstance(days_csv, str):
        return 0

    values = []
    for r in days_csv.split(','):
        cleaned = r.strip()
        if not cleaned:
            continue
        try:
            val = int(cleaned)
            if val >= 0:
                values.append(val)
        except (ValueError, TypeError):
            continue

    if not values:
        return 0

    return sum(values) // len(values)


def payable_fee(text):
    """
    Calculates payable fee after 18% tax and discount.
    Expected format: "fee|discount" (e.g. "6000|500")
    Formula: max(float(fee) * 1.18 - float(discount), 0.0)
    Returns: float payable fee, or 0.0 if invalid.
    """
    if not text or not isinstance(text, str):
        return 0.0

    parts = text.split('|')
    if len(parts) != 2:
        return 0.0

    fee_str, discount_str = parts
    fee_str = fee_str.strip()
    discount_str = discount_str.strip()

    try:
        fee = float(fee_str)
        discount = float(discount_str)
        if fee < 0 or discount < 0:
            return 0.0
        total = fee * 1.18 - discount
        return round(max(total, 0.0), 2)
    except (ValueError, TypeError, OverflowError):
        return 0.0


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
