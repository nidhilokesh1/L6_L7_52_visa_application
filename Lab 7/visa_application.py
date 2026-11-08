def parse_application(text):
    visa, entries = text.split(':')
    return visa.strip().title(), int(entries)

def processing_average(days_csv):
    values = [int(r) for r in days_csv.split(',')]
    return sum(values) // len(values)

def payable_fee(text):
    fee, discount = text.split('|')
    total = float(fee) * 1.18 - float(discount)
    return max(total, 0)

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
