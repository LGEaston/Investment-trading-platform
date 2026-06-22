import socket
import mysql.connector
import pickle

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
PORT = 5000 # <------- change the PORT according to your port
ADDRESS = (HOST, PORT)

server_socket.bind(ADDRESS)

server_socket.listen(1)

print("Server is listening for connection...")

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root', # <------- change the user according to your name name chosen
    'password': '', # <------- change password according to your database password chosen
    'database': 'investment' # <------- change the database name according to your database name chosen
}

# Check if the username and password combination exists in the client table
def check_credentials(cursor, username, password):
    cursor.execute("SELECT * FROM client WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    return result is not None

# When signing up, insert_client() fucntion inserts a new client record and return the generated clientID
def insert_client(cursor, username, password, initial_investment_cash, total_cash_to_invest):
    cursor.execute("""
        INSERT INTO client (username, password, InitialInvestmentCash, TotalCashToInvest, TotalInvestmentValue, TotalGainOrLoss)
        VALUES (%s, %s, %s, %s, 0, 0)
    """, (username, password, initial_investment_cash, total_cash_to_invest))
    # last row id gives the id of the last row in the client table
    client_id = cursor.lastrowid
    return client_id

while True:
    # Accept client connection
    client_socket, client_address = server_socket.accept()

    # Connect to the database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    # Receive client choice (signup or login)
    choice = client_socket.recv(1024).decode()
    print(choice)

    finish_login = False

    # Allow client data to be inserted when first creation of account
    allow_send_id_when_signup = False
    clientID_list = []
    username_list = []
    password_list = []

    while finish_login != True:
        if choice == 'signup':
            # Receive username and password from client
            username = client_socket.recv(1024).decode()
            password = client_socket.recv(1024).decode()

            # Check if the username and password exist in the database
            if check_credentials(cursor, username, password):
                client_socket.send(b'Signup failed. Username or password already exists.')

            else:
                # Insert client record and get the generated clientID
                initial_investment_cash = 0
                total_cash_to_invest = initial_investment_cash
                client_id = insert_client(cursor, username, password, initial_investment_cash, total_cash_to_invest)
                db.commit()
                clientID_list.append(client_id)
                client_socket.send(b'Sign up successful!')
                allow_send_id_when_signup = True

                finish_login = True

        elif choice == 'login':
            # Receive username and password from client
            username = client_socket.recv(1024).decode()
            print(username)
            password = client_socket.recv(1024).decode()
            print(password)

            # Check if the username and password exist in the database
            if check_credentials(cursor, username, password):
                client_socket.send(b'Login successful!')
                finish_login = True
            else:
                client_socket.send(b'Login failed. Incorrect username or password.')

    print("Login finished!")
    print(clientID_list)

    # If user signs up for the first time, the clientID is sent
    # to be displayed once the user gets a successful sign up
    if allow_send_id_when_signup == True:
        send_client_id = clientID_list[0]
        client_id_pickle = pickle.dumps(send_client_id)
        client_socket.send(client_id_pickle)

    # For Main Menu queries -----------------
    # Sending client info after login
    query_retrieve_client_info = client_socket.recv(1024).decode()
    cursor.execute(query_retrieve_client_info)
    retrieve_client_info = cursor.fetchall()
    print(retrieve_client_info)
    client_info_tuple = pickle.dumps(retrieve_client_info)
    client_socket.send(client_info_tuple)

    # Sending commodity table info after main menu
    query_retrieve_commodity_info = client_socket.recv(1024).decode()
    cursor.execute(query_retrieve_commodity_info)
    retrieve_commodity_info = cursor.fetchall()
    print(retrieve_commodity_info)
    commodity_table_info_tuple = pickle.dumps(retrieve_commodity_info)
    client_socket.send(commodity_table_info_tuple)

    # Start looping of received, retrieve and update commands from database and sending the retrieved data to client
    while True:
        query_command = client_socket.recv(1024).decode()
        print(query_command)
        if query_command == "Stop":
            break

        query_type = query_command.strip().split()[0].upper()
        print(query_type)
        if query_type == "SELECT":
            cursor.execute(query_command)
            retrieved_info = cursor.fetchall()
            tuple_data = pickle.dumps(retrieved_info)
            client_socket.send(tuple_data)
        elif query_type == "UPDATE":
            cursor.execute(query_command)
            db.commit()

        elif query_type == "INSERT":
            cursor.execute(query_command)
            db.commit()

    client_socket.close()

server_socket.close()
