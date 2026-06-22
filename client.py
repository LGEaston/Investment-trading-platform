import socket
import tkinter
from tkinter import messagebox
import pickle
from tkinter import ttk
from datetime import datetime

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
PORT = 5000 # <------- change the database name according to your port
ADDRESS = (HOST, PORT)

socket.connect(ADDRESS)

# ------Color Used------
BLACK_GREY = '#333333'
BLACK_COLOR = '#000000'
WHITE_COLOR = '#FFFFFF'

MEDIUM_PERSIAN_BLUE = '#045FB0'
NAVY_BLUE = '#050580'
SPANISH_YELLOW = '#F0AC0C'
POLISH_PINE = '#54AE93'
PEAR = '#CBD63C'

YELLOW_COLOR = '#F6EF00'
GREY_COLOR = '#929292'
GREEN = '#7CFF26'
ORANGE = '#FF9C03'
YELLOW = '#FFFF00'
BLUE = '#00E0FF'

# Quick way to send information to Server size using the send_message function
def send_message(sock, message):
    sock.send(message.encode())

# Quick way of receiving information from Server size using the receive_message function
def receive_message(sock):
    data = sock.recv(1024).decode()
    return data # <--- By returning data here, the response == "Login successful"

# Prompting the user for "Login" or "Sign up"
login_or_signup = tkinter.Tk()
login_or_signup.config(bg=BLACK_GREY)
login_or_signup.resizable(False, False)

def choose_login():
    choice = "login"
    send_message(socket, choice)
    login_or_signup.destroy()

def choose_signup():
    choice = "signup"
    send_message(socket, choice)
    login_or_signup.destroy()

# Creating Widgets
login_or_signup_label = tkinter.Label(login_or_signup, text="Choose to Login or Sign up", bg=BLACK_GREY, fg=SPANISH_YELLOW, font=("Arial", 30, 'bold'))
signup_button = tkinter.Button(login_or_signup, text="login", bg=MEDIUM_PERSIAN_BLUE, fg=WHITE_COLOR, font=("Arial", 20), height=1, width=10, command=choose_login)
login_button = tkinter.Button(login_or_signup, text="Sign up", bg=NAVY_BLUE, fg=WHITE_COLOR, font=("Arial", 20), height=1, width=10, command=choose_signup)

login_or_signup_label.pack()
login_button.pack(side=tkinter.LEFT, padx=100, pady=10)
signup_button.pack(side=tkinter.LEFT, padx=100, pady=10)

login_button.mainloop()


# GUI Main Window
window = tkinter.Tk()
window.title("Login Form")
# window.geometry('340x440')
window.geometry('500x450')
window.configure(bg=BLACK_GREY)

# Get [username, password] in list form when sign up or login successful, default credential_list = empty list
credential_list = []

# Login GUI
def login():
    # Send Both the username and password entered by user to the server side
    username = username_entry.get()
    password = password_entry.get()
    socket.send(username.encode())
    socket.send(password.encode())

    # Receiving the response from server side, if login or sign up was accepted
    response = receive_message(socket)

    if response == "Sign up successful!":
        #Get the clientID from clientID_list[0] send by server
        client_id_pickle = socket.recv(1024)
        client_id_received = pickle.loads(client_id_pickle)

        credential_list.append(username)
        credential_list.append(password)

        # Messagebox inform user that sign up was successful
        messagebox.showinfo(title="Sign up successful", message=f"You successfully signed up.\n"
                                                                f"Welcome!\n"
                                                                f"Your clientID is {client_id_received}")

        # Getting rid of the login frame after successful sign up
        login_frame.destroy()
        main_menu()

    if response == "Login successful!":
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        credential_list.append(username)
        credential_list.append(password)

        # Getting rid of the login frame after successful sign up
        login_frame.destroy()
        main_menu()

    elif response == "Login failed. Incorrect username or password.":
        # Display error message when incorrect login credentials
        # Added a face melting emoji --> \U0001FAE0
        messagebox.showerror(title="Error", message="Login failed. Incorrect username or password. \U0001FAE0")
    elif response == "Signup failed. Username or password already exists.":
        # Display error message when either username or password or both already exist
        messagebox.showerror(title="Error", message="Signup failed. Username or password already exists.")

# Get [clientID] in list form when retrieving data for client info, default client_id = empty list
client_id_list = []

# Main Menu Display
def main_menu():
    # The credential_list contains ['username', 'password]
    client_username = credential_list[0]
    client_password = credential_list[1]
    print(credential_list)

    # ---------- MAIN MENU GUI WIDGETS -----------
    # Menu Option buttons + Profile Info
    window.title("Main Menu")
    # Retrieve profile info of the user from database by using the username and the password previously entered
    query_retrieve_client_info = f"SELECT * FROM client WHERE username = '{client_username}' AND password = '{client_password}'"

    socket.send(query_retrieve_client_info.encode())
    client_info_pickle = socket.recv(1024)
    client_info_data = pickle.loads(client_info_pickle)

    # Using the tuple received from server and assigning each element inside tuple to a variable
    clientID = client_info_data[0][0]

    # append value for clientID to client_id_list to be reused outside the invest function
    client_id_list.append(clientID)

    total_investment_value = client_info_data[0][5]
    total_cash_to_invest = client_info_data[0][4]
    total_gain_loss = client_info_data[0][6]


    # Input a variable inside the Label
    msg = tkinter.StringVar()
    msg.set(f"clientID = {clientID}\n"
            f"Total Investment Value = £{total_investment_value}\n"
            f"Total Cash to Invest = £{total_cash_to_invest}\n"
            f"Total Gain/Loss = £{total_gain_loss}")

    # client_profile displays the client profile info on the GUI main menu
    client_profile = tkinter.Label(window, textvariable=msg, bg=BLACK_GREY, fg=WHITE_COLOR, font=("Arial", 16))
    client_profile.pack(pady=10)

    def update_balance_labels():
        # To retrieve client_profile info from the database again
        query_retrieve_client_info = f"SELECT * FROM client WHERE username = '{client_username}' AND password = '{client_password}'"
        socket.send(query_retrieve_client_info.encode())
        client_info_pickle = socket.recv(1024)
        client_info_data = pickle.loads(client_info_pickle)

        initial_investment_cash = client_info_data[0][3]
        total_investment_value = client_info_data[0][5]
        total_cash_to_invest = client_info_data[0][4]
        total_gain_loss = client_info_data[0][6]

        msg.set(f"clientID = {clientID}\n"
                f"Initial Investment Cash = £{initial_investment_cash}\n"
                f"Total Investment Value = £{total_investment_value}\n"
                f"Total Cash to Invest = £{total_cash_to_invest}\n"
                f"Total Gain/Loss = £{total_gain_loss}")

    # Update the values through the REFRESH button
    def refresh_clicked_button():
        update_balance_labels()

    # The REFRESH, Invest now, Portfolio Viewing and Pay in/ Withdraw button GUI Section
    refresh_button = tkinter.Button(window, text="REFRESH", bg=GREY_COLOR, fg=YELLOW_COLOR, font=("Arial", 16), command=refresh_clicked_button)
    refresh_button.pack(pady=10)

    invest_now_button = tkinter.Button(window, text="Invest now", bg=GREY_COLOR, fg=GREEN, font=("Arial", 16), command=invest)
    invest_now_button.pack(pady=10)

    portfolio_viewing_button = tkinter.Button(window, text="Portfolio Viewing", bg=GREY_COLOR, fg=BLUE, font=("Arial", 16), command=portfolio_viewing)
    portfolio_viewing_button.pack()

    payIn_button = tkinter.Button(window, text="Pay in/Withdraw", bg=GREY_COLOR, fg=WHITE_COLOR, font=("Arial", 16), command=pay_in_or_withdraw)
    payIn_button.pack(pady=10)

    initial_investment_button = tkinter.Button(window, text="Initial Investment Cash", bg=YELLOW_COLOR, fg=BLACK_COLOR, font=("Arial", 16), command=initial_investment_cash)
    initial_investment_button.pack(pady=10)


# "Invest now" Option
def invest():
    # Get clientID from the client_id_list to be able to use inside Invest Option
    clientID = client_id_list[0]

    # Retrieving all commodity id and their corresponding name and price
    query_retrieve_commodity_info = "SELECT * FROM commodity"
    socket.send(query_retrieve_commodity_info.encode())
    commodity_info_pickle = socket.recv(1024)
    commodity_table_info_data = pickle.loads(commodity_info_pickle)

    invest_window = tkinter.Tk()
    invest_window.title('Select Commodity to Buy/Sell')
    invest_window.geometry('700x550')
    invest_window.configure(bg=BLACK_GREY)

    # define columns
    columns = ('commodityID', 'commodityName', 'commodityPrice')
    table = ttk.Treeview(invest_window, columns=columns, show='headings')
    style = ttk.Style(invest_window)

    style.theme_use("clam")
    style.configure("Treeview", font=('Arial', 14))

    # Configuring heading of Treeview widget
    style.configure('Treeview.Heading', background=MEDIUM_PERSIAN_BLUE, foreground=WHITE_COLOR, font=('Arial', 15))

    # define headings for table
    table.heading('commodityID', text='commodityID')
    table.heading('commodityName', text='Commodity Name')
    table.heading('commodityPrice', text='Commodity Price')

    number_of_rows = len(commodity_table_info_data)
    commodity = []
    for element in range(number_of_rows):
        commodity_id = commodity_table_info_data[element][0]
        commodity_name = commodity_table_info_data[element][1]
        commodity_price = commodity_table_info_data[element][2]

        commodity.append((commodity_id, commodity_name, commodity_price))

    # add data to treeview
    for item in commodity:
        table.insert('', tkinter.END, values=item)

    # Constantly updates the Commodity Name and Commodity Price when selecting a row on the table
    def update_price(event):
        selection = table.focus()
        selected_item = table.item(selection)

        crypto_selected = selected_item['values']
        print(crypto_selected)
        commodityName = selected_item['values'][1]
        commodityPrice = selected_item['values'][2]
        commodity_name_label.configure(text=f'Commodity Name: {commodityName}')
        price_label.configure(text=f'Commodity Price: {commodityPrice}')

        commodityID = selected_item['values'][0]
        return commodityID

    # binding the selection of a row to the update_price function
    table.bind('<<TreeviewSelect>>', update_price)

    table.grid(row=0, column=0, sticky='news')
    # table.pack(fill=tkinter.BOTH, expand=True)

    # Commodity Name Label
    commodity_name_label = tkinter.Label(invest_window, text='Commodity Name: -', bg=BLACK_GREY, fg=WHITE_COLOR, font=('Arial', 20))
    commodity_name_label.grid(row=1, column=0, pady=10, sticky='w')

    # Commodity Price Label
    price_label = tkinter.Label(invest_window, text='Price: -', bg=BLACK_GREY, fg=WHITE_COLOR, font=('Arial', 20))
    price_label.grid(row=2, column=0, pady=10, sticky='w')

    # Commodity Quantity entered Label
    quantity_label = tkinter.Label(invest_window, text='Quantity', bg=BLACK_GREY, fg=WHITE_COLOR, font=('Arial', 20))
    quantity_label.grid(row=3, column=0, pady=10, sticky='w')

    # Commodity Quantity entered Entry
    quantity_entry = tkinter.Entry(invest_window, font=('Arial', 20))
    # quantity_entry.grid(row=3, column=1, pady=10, sticky='e')
    quantity_entry.place(x=150, y=360)

    # Function that retrieves and returns the "Total Investment Value"
    def get_client_total_investment_value():
        query_retrieve_client_info = f"SELECT * FROM Client WHERE clientID = {clientID}"
        socket.send(query_retrieve_client_info.encode())
        client_info_pickle = socket.recv(1024)
        client_row_info_data = pickle.loads(client_info_pickle)

        total_investment_value = client_row_info_data[0][5]

        return total_investment_value

    # Function that retrieves and returns the "Total Cash to Invest"
    def get_total_cash_to_invest():
        query_retrieve_client_info = f"SELECT * FROM Client WHERE clientID = {clientID}"
        socket.send(query_retrieve_client_info.encode())
        client_info_pickle = socket.recv(1024)
        client_row_info_data = pickle.loads(client_info_pickle)

        total_cash_to_invest = client_row_info_data[0][4]

        return total_cash_to_invest

    # Function that retrieves and returns the "Initial Investment Value"
    def get_client_initial_investment_value():
        query_retrieve_client_info = f"SELECT * FROM Client WHERE clientID = {clientID}"
        socket.send(query_retrieve_client_info.encode())
        client_info_pickle = socket.recv(1024)
        client_row_info_data = pickle.loads(client_info_pickle)

        initial_investment_value = client_row_info_data[0][3]

        return initial_investment_value

    # Function that retrieves and returns the "Total Gain/Loss"
    def get_client_total_gain_loss():
        query_retrieve_client_info = f"SELECT * FROM Client WHERE clientID = {clientID}"
        socket.send(query_retrieve_client_info.encode())
        client_info_pickle = socket.recv(1024)
        client_row_info_data = pickle.loads(client_info_pickle)

        total_gain_loss = client_row_info_data[0][6]

        return total_gain_loss

    # Function checks if the user has sufficient cash_to_invest before allowing the purchase of number of commodity
    # entered by the user.
    def check_sufficient_funds(selected_item):
        #Obtain the data following data from table Client in database
        cash_to_invest = float(get_total_cash_to_invest())
        total_investment_value = float(get_client_total_investment_value())
        print(f"Total investment value  = {total_investment_value}")
        total_gain_loss = float(get_client_total_gain_loss())
        initial_investment_value = float(get_client_initial_investment_value())

        # print(cash_to_invest)
        commodity_quantity = float(quantity_entry.get())
        commodity_price = float(selected_item['values'][2])

        # Total cost of commodity to be purchased calculation
        cost = commodity_quantity * commodity_price
        new_cash_to_invest = 0
        updated_investment_value = 0

        # Validates if transaction will be recorded inside the Portfolio
        # Set by Default False therefore unless cash_to_invest >= Cost is True, the transaction will be recorded inside
        # The portfolio table in the database
        allow_transaction_record = False

        if cash_to_invest >= cost:
            new_cash_to_invest = cash_to_invest - cost
            print(new_cash_to_invest)
            # Send change to database for table client: TotalCashToInvest, TotalInvestmentValue, TotalGainOrLoss
            query_update_client_cash_to_invest = f"UPDATE Client SET TotalCashToInvest = {new_cash_to_invest} WHERE clientID = {clientID}"
            socket.send(query_update_client_cash_to_invest.encode())
            # Reevaluate the total_investment_value
            updated_investment_value = total_investment_value + cost

            # Update the Total Investment Value in the Database by the updated_investment_value calculated
            query_update_client_total_investment_value = f"UPDATE Client SET TotalInvestmentValue = {updated_investment_value} WHERE clientID = {clientID}"
            socket.send(query_update_client_total_investment_value.encode())

            # messagebox informs the user of successful PURCHASE transaction
            messagebox.showinfo("Success", "Purchase successful!")
            allow_transaction_record = True

        else:
            # messagebox informs the user of unsuccessful PURCHASE transaction
            messagebox.showerror("Error", "Insufficient funds")

        # Calculate gain/loss = (cash to invest + total investment value) - initial investment value
        new_gain_or_loss = (new_cash_to_invest + updated_investment_value) - initial_investment_value
        query_update_client_gain_or_loss = f"UPDATE Client SET TotalGainOrLoss = {new_gain_or_loss} WHERE clientID = {clientID}"
        socket.send(query_update_client_gain_or_loss.encode())

        # INSERT into Portfolio the new purchase if allow_transaction_record is True
        if allow_transaction_record is True:
            commodityID = update_price(selected_item)
            print(commodityID)
            current_date = datetime.now()
            formatted_date = current_date.strftime("%Y-%m-%d")
            print(formatted_date)
            query_insert_transaction = f"INSERT INTO portfolio (clientID, commodityID, DateOfTransaction, typeOfTransaction, quantity, Cost) VALUES ({clientID}, {commodityID}, '{formatted_date}', 'BUY', {commodity_quantity}, {cost})"
            print(query_insert_transaction)
            socket.send(query_insert_transaction.encode())

    # Once the quantity is entered and the BUY button pressed, the user gets a pop up that displays the Commodity Name,
    # the Commodity Unit Price and the Total cost of the transaction
    def open_buy_window():
        selection = table.focus()
        selected_item = table.item(selection)
        chosen_commodity_name = selected_item['values'][1]
        the_commodity_price = float(selected_item['values'][2])
        commodity_quantity = float(quantity_entry.get())
        buy_window = tkinter.Toplevel(invest_window)
        buy_window.title('Buy')
        buy_window.geometry('300x300')
        buy_window.configure(bg=BLACK_GREY)
        buy_window_label = tkinter.Label(buy_window, text=f'Commodity Name: {chosen_commodity_name}\nPrice: {the_commodity_price}\nQuantity: {commodity_quantity}', bg=BLACK_GREY, fg=WHITE_COLOR, font=('Arial', 16))
        buy_window_label.pack(pady=20)

        # Cost calculation
        cost = commodity_quantity * the_commodity_price
        cost_label = tkinter.Label(buy_window, text=f"Cost: ${cost}", bg=BLACK_GREY, fg=WHITE_COLOR, font=('Arial', 16))
        cost_label.pack()

        # "Confirm&Pay" button --> calls the check_sufficient_funds() function to check if user's fund are enough
        confirm_pay_button = tkinter.Button(buy_window, text="Confirm&Pay", bg='green', fg=WHITE_COLOR, font=('Arial',16), command=lambda: check_sufficient_funds(selected_item))
        confirm_pay_button.pack()

        # Edit button closes the buy_window for user to be able to edit the commodity chosen and quantity entered
        def edit_button():
            buy_window.destroy()

        # Cancel button closes the Invest window
        def cancel_button():
            invest_window.destroy()

        # "Edit" button GUI
        edit_button = tkinter.Button(buy_window, text="Edit", font=('Arial',16), command=edit_button)
        edit_button.pack()

        # "Return" button GUI
        cancel_button = tkinter.Button(buy_window, text="Cancel", font=('Arial',16), command=cancel_button)
        cancel_button.pack()

    # Buy Button GUI
    buy_button = tkinter.Button(invest_window, text='Buy', height=1, width=3, bg="green", fg=WHITE_COLOR, font=('Arial', 20), command=open_buy_window)
    buy_button.grid(row=4, column=0, padx=20, pady=10, sticky='e')

    # Function checks if the user has sufficient commodities before allowing the sale of number of commodity
    # entered by the user.
    def quantity_commodity_in_possession(selected_item):
        commodityID = update_price(selected_item)

        # Find total quantity for the commodityID bought
        query_commodity_buy_quantity = f"SELECT quantity FROM Portfolio WHERE clientID = {clientID} AND typeOfTransaction = 'BUY' AND commodityID = {commodityID}"
        socket.send(query_commodity_buy_quantity.encode())
        quantity_buy_info_pickle = socket.recv(1024)
        commodity_rows_buy_data = pickle.loads(quantity_buy_info_pickle)

        # creates a total_buy_commodities outside of the for loop and assign it an initial default value of 0
        total_buy_commodities = 0
        number_of_buy = len(commodity_rows_buy_data)
        for row in range(number_of_buy):
            # Calculation to add up all BUY commodity in the database for the user's clientID
            total_buy_commodities = total_buy_commodities + int(commodity_rows_buy_data[row][0])

        print(f"Total BUY commodities = {total_buy_commodities}")

        # Find total quantity for the commodityID bought
        query_commodity_sell_quantity = f"SELECT quantity FROM Portfolio WHERE clientID = {clientID} AND typeOfTransaction = 'SELL' AND commodityID = {commodityID}"
        socket.send(query_commodity_sell_quantity.encode())
        quantity_sell_info_pickle = socket.recv(1024)
        commodity_rows_sell_data = pickle.loads(quantity_sell_info_pickle)

        # create a total_sell_commodities outside of the for loop and assign it an initial default value of 0
        total_sell_commodities = 0
        number_of_sell = len(commodity_rows_sell_data)
        for row in range(number_of_sell):
            # Calculation to add up all BUY commodity in the database for the user's clientID
            total_sell_commodities = total_sell_commodities + int(commodity_rows_sell_data[row][0])

        print(f"Total SELL commodities = {total_sell_commodities}")

        # Calculation for total commodities in possession for selected commodityID and given clientID
        total_assets = total_buy_commodities - total_sell_commodities

        print(f"Total Assets commodities = {total_assets}")

        return total_assets

    def check_sufficient_commodity(selected_item):

        # Obtain the data following data from table Client in database
        total_investment_value = float(get_client_total_investment_value())
        print(f"Total investment value  = {total_investment_value}")
        initial_investment_value = float(get_client_initial_investment_value())

        commodity_quantity_to_sell = int(quantity_entry.get())
        commodity_selling_price = float(selected_item['values'][2])

        # Get total commodity in possession
        total_assets = quantity_commodity_in_possession(selected_item)

        # Selling cost calculation
        sell_cost = commodity_quantity_to_sell * commodity_selling_price

        # allow_transaction_record allow for transaction to be recorded only if commodity_quantity_to_sell less than
        # or equal to the total_assets
        allow_transaction_record = False

        if commodity_quantity_to_sell <= total_assets:
            # Increase TotalCashToInvest in client table by
            query_update_client_cash_to_invest = f"UPDATE Client SET TotalCashToInvest = TotalCashToInvest + {sell_cost} WHERE clientID = {clientID}"
            socket.send(query_update_client_cash_to_invest.encode())

            # Reevaluate the total_investment_value
            query_update_client_total_investment_value = f"UPDATE Client SET TotalInvestmentValue = TotalInvestmentValue - {sell_cost} WHERE clientID = {clientID}"
            socket.send(query_update_client_total_investment_value.encode())

            allow_transaction_record = True
            # messagebox notifies the user that SALE was successful
            messagebox.showinfo("Success", "Sale successful!")

        else:
            # messagebox notifies the user that SALE was unsuccessful
            messagebox.showerror("Error", "Insufficient commodity")

        new_total_investment_value = float(get_client_total_investment_value())
        new_cash_to_invest = float(get_total_cash_to_invest())

        # Calculate gain/loss = (cash to invest + total investment value) - initial investment value
        new_gain_or_loss = (new_cash_to_invest + new_total_investment_value) - initial_investment_value
        query_update_client_gain_or_loss = f"UPDATE Client SET TotalGainOrLoss = {new_gain_or_loss} WHERE clientID = {clientID}"
        socket.send(query_update_client_gain_or_loss.encode())

        # INSERT into Portfolio new purchase if True
        if allow_transaction_record is True:
            commodityID = update_price(selected_item)
            current_date = datetime.now()
            formatted_date = current_date.strftime("%Y-%m-%d")
            query_insert_transaction = f"INSERT INTO portfolio (clientID, commodityID, DateOfTransaction, typeOfTransaction, quantity, Cost) VALUES ({clientID}, {commodityID}, '{formatted_date}', 'SELL', {commodity_quantity_to_sell}, {sell_cost})"

            socket.send(query_insert_transaction.encode())

    # Window when the Sell Button is pressed
    def open_sell_window():
        selection = table.focus()
        selected_item = table.item(selection)
        chosen_commodity_name = selected_item['values'][1]
        the_commodity_price = float(selected_item['values'][2])
        commodity_quantity = float(quantity_entry.get())

        # Sell window GUI
        sell_window = tkinter.Toplevel(invest_window)
        sell_window.title('Buy')
        sell_window.geometry('300x300')
        sell_window.configure(bg=BLACK_GREY)
        sell_window_label = tkinter.Label(sell_window, text=f'Commodity Name: {chosen_commodity_name}\nSelling unit Price: £{the_commodity_price}\nSelling Quantity: {commodity_quantity}', bg=BLACK_GREY, fg=WHITE_COLOR, font=('Arial', 16))
        sell_window_label.pack(pady=20)

        # Cost for sale of commodities calculation
        cost = commodity_quantity * the_commodity_price
        cost_label = tkinter.Label(sell_window, text=f"Selling Cost: ${cost}", bg=BLACK_GREY, fg=WHITE_COLOR, font=('Arial', 16))
        cost_label.pack()

        # "Confirm&Sell" button
        # Remove the check_sufficient_funds to check_sufficient_assets
        confirm_pay_button = tkinter.Button(sell_window, text="Confirm&Sell", bg='green', fg=WHITE_COLOR, font=('Arial',16), command=lambda: check_sufficient_commodity(selected_item))
        confirm_pay_button.pack()

        def edit_button():
            sell_window.destroy()

        def cancel_button():
            invest_window.destroy()

        # "Edit" button
        edit_button = tkinter.Button(sell_window, text="Edit", font=('Arial',16), command=edit_button)
        edit_button.pack()

        # "Return" button
        cancel_button = tkinter.Button(sell_window, text="Cancel", font=('Arial',16), command=cancel_button)
        cancel_button.pack()

    # Sell Button
    sell_button = tkinter.Button(invest_window, text='Sell', height=1, width=3, bg="red", fg=WHITE_COLOR, font=('Arial', 20), command=open_sell_window)
    sell_button.grid(row=4, column=1, pady=10, sticky='w')

    invest_window.mainloop()

#---------Pay In/withdraw Option----------
def pay_in_or_withdraw():
    # Get clientID from the client_id_list to be able to use inside Pay in/Withdraw Option
    clientID = client_id_list[0]

    # Get user balance info
    query_retrieve_client_info = f"SELECT * FROM client WHERE clientID = {clientID}"
    socket.send(query_retrieve_client_info.encode())
    client_info_pickle = socket.recv(1024)
    client_info_data = pickle.loads(client_info_pickle)

    # Assign the following values to variable: TotalCashToInvest, index 4
    # clientID = client_info_data[0][0]
    total_cash_to_invest = client_info_data[0][4]

    pay_withdraw_window = tkinter.Tk()
    pay_withdraw_window.title('Money in/out')
    pay_withdraw_window.geometry('400x300')
    pay_withdraw_window.resizable(False, False)
    pay_withdraw_window.configure(bg='#333333')

    # Display the current Cash to Invest balance in user's account
    current_balance = tkinter.Label(pay_withdraw_window, text=f"Current Balance: £{total_cash_to_invest}", bg=BLACK_GREY, fg=PEAR, font=('Arial', 20))
    current_balance.pack()

    amount_label = tkinter.Label(pay_withdraw_window, text=f"Enter the amount(£): ", bg=BLACK_GREY, fg=WHITE_COLOR, width=200, font=('Arial', 16))
    amount_label.pack(padx=100)
    amount_entry = tkinter.Entry(pay_withdraw_window, width=200, font=('Arial', 16))
    amount_entry.pack(padx=100)

    # pay_in() function when user want to insert money into their account
    def pay_in():
        amount_pay_in = amount_entry.get()
        query_amount_pay_in = f"UPDATE Client SET TotalCashToInvest = TotalCashToInvest + {amount_pay_in} WHERE clientID = {clientID}"
        socket.send(query_amount_pay_in.encode())
        messagebox.showinfo("Transfer successful", f"Transfer of £{amount_pay_in} successful!")
        pay_withdraw_window.destroy()

    # pay_in() function when user want to remove money from their account
    def withdraw():
        amount_to_withdraw = float(amount_entry.get())
        if amount_to_withdraw <= total_cash_to_invest:
            query_amount_to_withdraw = f"UPDATE Client SET TotalCashToInvest = TotalCashToInvest - {amount_to_withdraw} WHERE clientID = {clientID}"
            socket.send(query_amount_to_withdraw.encode())
            messagebox.showinfo("Transaction successful", f"Withdrawal of £{amount_to_withdraw} successful!")
            pay_withdraw_window.destroy()
        else:
            messagebox.showerror("Transaction failed", f"Insufficient funds")

    pay_in_button = tkinter.Button(pay_withdraw_window, text="Pay In", bg="green", fg=BLACK_COLOR, width=10, height=5, font=('Arial', 16), command=pay_in)
    pay_in_button.pack(padx=20, pady=5, side=tkinter.LEFT)
    withdraw_window = tkinter.Button(pay_withdraw_window, text="Withdraw", bg="red", fg=BLACK_COLOR,width=10, height=5, font=('Arial', 16), command=withdraw)
    withdraw_window.pack(padx=30, pady=5, side=tkinter.RIGHT)

    pay_withdraw_window.mainloop()

#---------Portfolio Option----------
# portfolio_viewing to display all BUY and SELL transaction made by the user
def portfolio_viewing():
    # Get clientID from the client_id_list to be able to use inside portfolio Option
    clientID = client_id_list[0]

    # Retrieve all Portfolio info from the database for the given clientID
    query_retrieve_portfolio_info = f"SELECT * FROM portfolio WHERE clientID = {clientID}"
    socket.send(query_retrieve_portfolio_info.encode())
    portfolio_info_pickle = socket.recv(1024)
    portfolio_table_info_data = pickle.loads(portfolio_info_pickle)

    portfolio_window = tkinter.Tk()
    portfolio_window.title('Select Commodity to Buy/Sell')
    portfolio_window.geometry('1200x300')
    portfolio_window.configure(bg=BLACK_GREY)

    # define columns
    columns = ('transactionID', 'commodityID', 'DateOfTransaction', 'typeOfTransaction', 'quantity', 'cost')
    table = ttk.Treeview(portfolio_window, columns=columns, show='headings')

    style = ttk.Style(portfolio_window)

    style.theme_use("clam")
    style.configure("Treeview", font=('Arial', 14))

    # Configuring heading of Treeview widget
    style.configure('Treeview.Heading', background=MEDIUM_PERSIAN_BLUE, foreground=WHITE_COLOR, font=('Arial', 15))

    # define headings for portfolio
    table.heading('transactionID', text='Transaction ID')
    table.heading('commodityID', text='Commodity ID')
    table.heading('DateOfTransaction', text='Date of Transaction')
    table.heading('typeOfTransaction', text='Type of Transaction')
    table.heading('quantity', text='Quantity')
    table.heading('cost', text='Cost(£)')

    number_of_rows = len(portfolio_table_info_data)

    portfolio = []
    for element in range(number_of_rows):
        transaction_id = portfolio_table_info_data[element][0]
        commodity_id = portfolio_table_info_data[element][2]
        date_of_transaction = portfolio_table_info_data[element][3]
        type_of_transaction = portfolio_table_info_data[element][4]
        quantity = portfolio_table_info_data[element][5]
        cost = portfolio_table_info_data[element][6]

        portfolio.append((transaction_id, commodity_id, date_of_transaction, type_of_transaction, quantity, cost))

    # add data to treeview
    for item in portfolio:
        table.insert('', tkinter.END, values=item)

    table.bind('<<TreeviewSelect>>')

    table.grid(row=0, column=0, sticky='news')

# Allow for user to input their initial Investment
def initial_investment_cash():
    clientID = client_id_list[0]

    # Get user balance info
    query_retrieve_client_info = f"SELECT * FROM client WHERE clientID = {clientID}"
    socket.send(query_retrieve_client_info.encode())
    client_info_pickle = socket.recv(1024)
    client_info_data = pickle.loads(client_info_pickle)

    # Assign the following values to variable: TotalCashToInvest, index 4
    # clientID = client_info_data[0][0]
    initial_investment_cash = client_info_data[0][4]

    # Creation of the initial invest window GUI
    initial_invest_window = tkinter.Tk()
    initial_invest_window.title("Initial Investment")
    initial_invest_window.configure(bg=BLACK_GREY)
    initial_invest_window.geometry('300x150')

    initial_invest_label = tkinter.Label(initial_invest_window, text="Enter your initial Investment:", bg=BLACK_GREY, fg=WHITE_COLOR, font=('Arial', 16))
    initial_invest_label.pack(pady=10)
    initial_invest_entry = tkinter.Entry(initial_invest_window, font=('Arial', 16))
    initial_invest_entry.pack()

    # Updates the Database for the InitialInvestmentCash and TotalCashToInvest according to these requirements:
    # - initial investment cash is initially zero
    # - initial cash to invest is not a negative value
    def submit_initial_investment():
        initial_investment_input = float(initial_invest_entry.get())

        # Ensures that the user input the initial investment cash only once
        if initial_investment_cash != 0:
            messagebox.showerror("Transfer Unauthorized",
                                 f"Transfer for initial investment cash can only occur once when the user signs up for the first time.")

        elif initial_investment_input >= 0:

            query_transfer_initial_investment = f"UPDATE Client SET InitialInvestmentCash = {initial_investment_input}, TotalCashToInvest = {initial_investment_input} WHERE clientID = {clientID}"
            print(query_transfer_initial_investment)

            socket.send(query_transfer_initial_investment.encode())

            initial_invest_window.destroy()

        else:
            messagebox.showerror("Invalid Input",
                                 f"Initial investment cash has to be a positive input.")

    transfer_button = tkinter.Button(initial_invest_window, text="TRANSFER", bg=PEAR, font=('Arial', 16), command=submit_initial_investment)
    transfer_button.pack(pady=10)

# ---------- LOGIN/SIGN UP GUI WIDGETS -----------
login_frame = tkinter.Frame(bg=BLACK_GREY)

# Creating Widgets
login_label = tkinter.Label(login_frame, text="ACCOUNT", bg=BLACK_GREY, fg=MEDIUM_PERSIAN_BLUE, font=("Arial", 50, 'bold'))
username_label = tkinter.Label(login_frame, text="username", bg=BLACK_GREY, fg=WHITE_COLOR, font=("Arial", 16))
username_entry = tkinter.Entry(login_frame, font=("Arial", 16))
password_label = tkinter.Label(login_frame, text="password", bg=BLACK_GREY, fg=WHITE_COLOR, font=("Arial", 16))
password_entry = tkinter.Entry(login_frame, font=("Arial", 16))
login_button = tkinter.Button(login_frame, text="Enter", bg=POLISH_PINE, fg=BLACK_COLOR, font=("Arial", 16), command=login)

# Placing widgets on screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20, padx=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20, padx=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

login_frame.pack()
window.mainloop()
socket.close()
