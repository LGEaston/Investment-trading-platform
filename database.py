import mysql.connector

# Connect to the MySQL server
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='investment' #<------ Change database to your database name
)

# Create an instance of the cursor
cursor = db.cursor()

# Create the client table
cursor.execute("""
        CREATE TABLE IF NOT EXISTS Client (
            clientID INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            password VARCHAR(50),
            InitialInvestmentCash DECIMAL(10,2),
            TotalCashToInvest DECIMAL(10,2),
            TotalInvestmentValue DECIMAL(10,2),
            TotalGainOrLoss DECIMAL(10,2)
        )
    """)

# Create the commodity table

# Read the crypto.text file
with open('crypto.txt', 'r') as file:
    lines = file.readlines()

# Extract the commodity name and price, convert price to integer
# data = [ Name(VARCHAR), Price(INT)]
crypto_data = [(line.split(',')[0].strip(), float(line.split(',')[1].replace('$', '').replace(',', ''))) for line in lines[1:8]]

# Create the Commodity table
create_table_query = """
    CREATE TABLE IF NOT EXISTS Commodity (
        CommodityID INT AUTO_INCREMENT,
        Name VARCHAR(20),
        Price Decimal(10,2),
        PRIMARY KEY (CommodityID)
    )
"""

cursor.execute(create_table_query)

# Insert cryptocurrencies data into the Commodity table
insert_crypto_query = "INSERT INTO Commodity (Name, Price) VALUES (%s, %s)"
cursor.executemany(insert_crypto_query, crypto_data)
db.commit()

# Insert the Ore data into the Commodity table
insert_ore_query = "INSERT INTO Commodity (Name, Price) VALUES (%s, %s)"
ore_data = [('Gold', 1971.70), ('Silver', 24.98)]
cursor.executemany(insert_ore_query, ore_data)
db.commit()

# Create the portfolio table
cursor.execute("""
        CREATE TABLE IF NOT EXISTS Portfolio (
            transactionID INT AUTO_INCREMENT PRIMARY KEY,
            clientID INT,
            commodityID INT,
            DateOfTransaction DATE,
            typeOfTransaction VARCHAR(4),
            quantity INT,
            Cost DECIMAL (10,2),
            FOREIGN KEY (clientID) REFERENCES Client(clientID),
            FOREIGN KEY (commodityID) REFERENCES Commodity(commodityID)
        )
    """)


# Close the database connection
cursor.close()
db.close()
