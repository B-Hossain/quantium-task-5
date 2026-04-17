import csv
import os

DATA_DIRECTORY = "./data"
OUTPUT_FILE_PATH = "./formatted_data.csv"
OUTPUT_HEADER = ["sales", "date", "region"]
TARGET_PRODUCT = "pink morsel"


def parse_sale(raw_price: str, quantity: str) -> float:
    unit_price = float(raw_price[1:])
    return unit_price * int(quantity)


def iter_input_rows(input_path: str):
    with open(input_path, "r") as input_file:
        reader = csv.reader(input_file)
        for row_index, input_row in enumerate(reader):
            if row_index == 0:
                continue
            yield input_row


def build_output_row(input_row):
    raw_price = input_row[1]
    quantity = input_row[2]
    transaction_date = input_row[3]
    region = input_row[4]
    sale = parse_sale(raw_price, quantity)
    return [sale, transaction_date, region]


def main():
    with open(OUTPUT_FILE_PATH, "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(OUTPUT_HEADER)

        for file_name in os.listdir(DATA_DIRECTORY):
            input_path = f"{DATA_DIRECTORY}/{file_name}"
            for input_row in iter_input_rows(input_path):
                product = input_row[0]
                if product == TARGET_PRODUCT:
                    writer.writerow(build_output_row(input_row))


if __name__ == "__main__":
    main()
