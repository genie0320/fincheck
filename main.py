import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from data_entry import get_amount, get_category, get_date, get_description


class CSV:
    CSV_FILE = "finance_data.csv"
    ITEMS = ["date", "amount", "category", "description"]
    FORMAT = "%Y-%m-%d"

    @classmethod
    def init_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)

        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.ITEMS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.ITEMS)
            writer.writerow(new_entry)

            print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filterd_df = df.loc[mask]

        if filterd_df.empty:
            print("No data in that period")
        else:
            print(
                f"Transaction from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}"
            )
            print(
                filterd_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}
                )
            )

            total_income = filterd_df[filterd_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filterd_df[filterd_df["category"] == "Expense"][
                "amount"
            ].sum()
            print("\n Summary : ")
            print(f"Total Income : ${total_income :.2f}")
            print(f"Total Expense : ${total_expense :.2f}")
            print(f"Total Balance : ${total_income-total_expense :.2f}")

        return filterd_df


def add():
    CSV.init_csv()
    date = get_date("Enter the date of the transaction :", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry(date, amount, category, description)


def plot_transaction(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("date")
    plt.ylabel("amount")
    plt.title("Income and Expense Over time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transaction and summary with in a date range")
        print("3. Exit")
        user_select = input("What can I do for you(1-3)? : ")

        if user_select == "1":
            add()

        elif user_select == "2":
            start_date = get_date("Enter the start date : ")
            end_date = get_date("Enter the end date : ")
            df = CSV.get_transactions(start_date, end_date)

            if input("Show graph? (y/n) :").lower() == "y":
                plot_transaction(df)

        elif user_select == "3":
            print("Exiting")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
