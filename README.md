<div align="center">

# 💹 Investment Portfolio Simulator

### A desktop investment simulator built with Python, Tkinter, MySQL and sockets

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

</div>

---

## 📖 About the Project
The **Investment Portfolio Simulator** is a Python desktop application that allows users to simulate investing in cryptocurrencies and precious metals.

Users can create an account, deposit virtual money, purchase or sell commodities, and view their transaction history.

The application follows a client-server architecture:

```text
Tkinter Client → Python Socket Server → MySQL Database
```

Cryptocurrency prices are collected using Selenium and Beautiful Soup.

---

## ✨ Features
- Create an account and log in
- Deposit and withdraw virtual money
- View available cryptocurrencies and precious metals
- Buy and sell commodities
- Check available investment cash
- View total investment value
- Calculate total gain or loss
- View previous portfolio transactions
- Store user and transaction information in MySQL
- Retrieve cryptocurrency prices through web scraping

---

## 🖥️ Application Preview
<p align="center">
  <img src="assets/app-preview.png" alt="Investment Portfolio Simulator preview" width="750">
</p>

> Add a screenshot of your application to an `assets` folder and name it `app-preview.png`.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Desktop graphical interface |
| MySQL | User, commodity and portfolio data |
| Python sockets | Client-server communication |
| Selenium | Loading cryptocurrency price data |
| Beautiful Soup | Parsing scraped HTML |
| XAMPP | Running the local MySQL database |

---

## 📁 Project Structure
```text
investment-portfolio-simulator/
│
├── client.py             # Tkinter interface and client logic
├── server.py             # Socket server and database communication
├── database.py           # Creates and populates database tables
├── crypto_webscraping.py # Retrieves cryptocurrency prices
├── crypto.txt            # Generated cryptocurrency data
├── requirements.txt      # Python dependencies
├── README.md

```

---

## 🗄️ Database Structure
The application uses an `investment` MySQL database with three main tables:

### Client

Stores user credentials and account balances.

### Commodity

Stores cryptocurrency and precious-metal information.

### Portfolio

Stores the user's buy and sell transactions.

---

## 🚀 Getting Started
### Prerequisites

Before running the project, install:

- Python 3
- Git
- Google Chrome
- XAMPP
- MySQL through XAMPP

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/investment-portfolio-simulator.git
cd investment-portfolio-simulator
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
beautifulsoup4
selenium
mysql-connector-python
```

### 3. Start MySQL

1. Open XAMPP.
2. Start **MySQL**.
3. Open phpMyAdmin.
4. Create a database named:

```text
investment
```

The default database configuration is:

```python
host="localhost"
user="root"
password=""
database="investment"
```

Update the settings in `database.py` and `server.py` when your MySQL configuration is different.

### 4. Retrieve cryptocurrency prices

```bash
python webscraping.py
```

This creates the `crypto.txt` file.

### 5. Prepare the database

```bash
python database.py
```

This creates the required tables and inserts the commodity information.

### 6. Start the server

```bash
python server.py
```

Keep this terminal open.

### 7. Start the client

Open another terminal and run:

```bash
python client.py
```

The login and sign-up window should appear.

---

## 🔄 Running Order

Run the files in this order:

```text
1. webscraping.py
2. database.py
3. server.py
4. client.py
```

The server must remain running while the client application is being used.

---

## ⚠️ Important Notice
This application was created for educational purposes and uses virtual investment funds. It does not provide real financial services or investment advice.

The current version stores passwords without production-level encryption and should not be deployed as a real financial application.

---

## 👩‍💻 Author

**Lisa Easton**

Created as a Python client-server and database development project.
