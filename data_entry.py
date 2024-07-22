from datetime import datetime

date_format = "%Y-%m-%d"
CATEGORY = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    date_input = input(prompt)
    if allow_default and not date_input:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_input, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in 'yyyy-mm-dd'.")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input('Enter the category ("I" for Income, "E" for Expense) :').upper()
    if category in CATEGORY:
        return CATEGORY[category]

    print('Invalid category. Please enter "I" for Income or "E"')
    return get_category()


def get_description():
    return input("Enter a description :")
