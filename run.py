import gspread 
from google.oauth2.service_account import Credentials
from pprint import pprint 
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS =Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT =gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)

def get_sales_data ():
    """
    Gets sales figures input from the user
    """
    while True: 
        print("Please Enter Sales data from the last market")
        print("data should be six numbers , seperated by commas ")
        print("Example: 10, 20 , 30 , 40 , 50 , 60 \n")
    
        data_str = input("Enter your data here : \n")
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid")
            break 

    return sales_data
def validate_data(values):
    """
    Ensures correct data is fed to the excel sheet . Raises value error if data does not match required structure.
    Checks 6 values and must be integers  
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required you provided {len(values)} "
            ) 
    except ValueError as e:
        print(f"Invalid data :{e} please try again \n")
        return False
    
    return True 
"""
def update_sales_worksheet(data):
   
    print("Updating sales work .... \n")
    sales_worksheet =SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully \n")

def update_surplus_worksheet(data):

    print("Updating surplus work .... \n")
    surplus_worksheet =SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("surplus worksheet updated successfully \n")
"""
def update_worksheet(data,worksheet):
    print(f"Updating {worksheet} worksheet ... \n")
    worksheet_to_update =SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated sucessfully \n ")

def calculate_surplus_data(sales_row):
    """
    Compare Sales with stock and calc surplus for each item type 
    """
    print("Calculating surplus data : .... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
 
    surplus_data = []
    for stock,sales in zip(stock_row,sales_row):
        surplus = int(stock) - sales 
        surplus_data.append(surplus)
    return surplus_data


def main():
    """
    Run all program functions 
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,"sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,"surplus")
print("Welcome to love sandwiches data automation")
main()


