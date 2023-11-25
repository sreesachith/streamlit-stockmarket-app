import mysql.connector
import pandas as pd
from config import HOST, USER, PASSWORD, PORT


connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    port=PORT,
)

cursor = connection.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS stockmarket')
cursor.execute('USE stockmarket')

def create_tables():
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS member (
            mid INT NOT NULL AUTO_INCREMENT UNIQUE,
            mname VARCHAR(20),
            pass VARCHAR(10),
            balance NUMERIC(20, 5),
            PRIMARY KEY(mname,pass)
        )
        ''')

        cursor.execute('''
        INSERT INTO member (mname, pass, balance) VALUES ('Shreya', 'abc', 100000.00)
        ''')

        cursor.execute('''
        INSERT INTO member (mname, pass, balance) VALUES ('Hiral Shah', '123', 50000.00)
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            P_ID INT AUTO_INCREMENT PRIMARY KEY,  
            name VARCHAR(100),  
            buy_price DECIMAL(10, 2),  
            curr_price DECIMAL(10, 2),
            Quantity INT,
            m_name VARCHAR(50)
        )
        ''')


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS company (
            comp_name VARCHAR(50),
            industry VARCHAR(50),
            curr_price FLOAT(2),
            open_price FLOAT(2),
            PRIMARY KEY(comp_name, curr_price)
        )
        ''')

        cursor.execute('''
        INSERT INTO company (comp_name, industry, curr_price, open_price) VALUES 
        ('Cipla', 'Pharmaceuticals', 105.25, 100.0),
        ('Wipro', 'Information Technology', 65.23, 60.0),
        ('Hindustan Unilever', 'Consumer goods', 564.78, 560.0)
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            comp_name VARCHAR(50),
            industry VARCHAR(50),
            curr_price FLOAT(2),
            open_price FLOAT(2),
            m_name VARCHAR(50),
            PRIMARY KEY(comp_name, m_name)
        )
        ''')
        
        
        
        
        connection.commit()
        
    except mysql.connector.Error as error:
        print("Error:", error)

    
          
        
def drop_procedure():
    try:
        cursor.execute("DROP PROCEDURE IF EXISTS update_curr_price")
        connection.commit()
    except mysql.connector.Error as error:
        print("Error:", error)

def create_function():
    cursor.execute('''
        CREATE PROCEDURE update_curr_price()
        BEGIN
            DECLARE random_value FLOAT;
            SET random_value = ((RAND() * 0.04) - 0.02);
        
            UPDATE company
            SET curr_price = curr_price * (1 + random_value); 
            
        END 
        ''')
    cursor.execute('''
            DROP TRIGGER IF EXISTS after_company_update;
        ''')
        
    cursor.execute('''
        CREATE TRIGGER after_company_update
        AFTER UPDATE ON company
        FOR EACH ROW
        BEGIN
            IF OLD.curr_price <> NEW.curr_price THEN
                UPDATE watchlist
                SET curr_price = NEW.curr_price
                WHERE comp_name = NEW.comp_name;
            END IF;
        END;
        ''')
    
    cursor.execute('''
            DROP TRIGGER IF EXISTS after_company_update_1;
        ''')
        
    cursor.execute('''
        CREATE TRIGGER after_company_update_1
        AFTER UPDATE ON company
        FOR EACH ROW
        BEGIN
            IF OLD.curr_price <> NEW.curr_price THEN
                UPDATE portfolio
                SET curr_price = NEW.curr_price
                WHERE name = NEW.comp_name;
            END IF;
        END;
        ''')
    connection.commit()





def is_username_taken(username):
    cursor.execute("SELECT * FROM member WHERE mname=%s", (username,))
    existing_user = cursor.fetchone()
    return existing_user is not None

# Function to add a new user to the Users table
def add_user(username, password):
    cursor.execute("INSERT INTO member (mname, pass, balance) VALUES (%s, %s, 0.0)", (username, password))
    connection.commit()
    
   

def verify_login(username, password):
        cursor.execute("SELECT * FROM member WHERE mname=%s AND pass =%s", (username, password))
        user = cursor.fetchone()  # Fetch the result to consume it
        if user:
            return True
        else:
            return False


def update_balance(username, password):
    cursor.execute("INSERT INTO member VALUES (%s, %s,0.0)", (username, password))
     

def view_watchlist(username):
    try:
        cursor.execute('''
            SELECT * FROM watchlist WHERE m_name = %s
        ''', (username,))
        watchlist = cursor.fetchall()
        return watchlist
    except mysql.connector.Error as error:
        print("Error:", error)


def view_portfolio(username):
    try:
        cursor.execute('''
            SELECT * ,(curr_Price*Quantity) AS investment, (curr_Price - buy_price) * Quantity AS gain FROM portfolio WHERE m_name = %s
        ''', (username,))
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as error:
        print("Error:", error)


def view_stock():
    try:
        cursor.execute("SELECT * FROM company")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as error:
        print("Error reading company data:", error)
        
def add_to_watchlist(comp_name, username):
    try:
        # Check if the stock exists in the watchlist table for the specific user
        cursor.execute("SELECT * FROM watchlist WHERE comp_name = %s AND m_name = %s", (comp_name, username))
        stock_data = cursor.fetchall()

        if stock_data:  # If the stock already exists in watchlist for this user, inform the user
            print(f"{comp_name} is already in the watchlist for {username}")
        else:
            # Check if the stock exists in the company table
            cursor.execute("SELECT * FROM company WHERE comp_name = %s", (comp_name,))
            company_data = cursor.fetchall()

            if company_data:  # If the stock exists in company, add it to the watchlist for this user
                if username:
                    # Assuming company_data contains the required columns from the company table
                    cursor.execute('''
                        INSERT INTO watchlist (comp_name, industry, curr_price, open_price, m_name)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (company_data[0][0], company_data[0][1], company_data[0][2], company_data[0][3], username))
                    connection.commit()
                    return True
                else:
                    print(f"User {username} does not exist.")
                    return False
            else:
                return False
    except mysql.connector.Error as error:
        print("Error:", error)
        
def add_to_portfolio(comp_name, username,quant):
    try:
        # Check if the stock exists in the watchlist table for the specific user
        cursor.execute("SELECT * FROM portfolio WHERE name = %s AND m_name = %s", (comp_name, username))
        stock_data = cursor.fetchall()

        if stock_data:  # If the stock already exists in watchlist for this user, inform the user
            print(f"{comp_name} is already in the watchlist for {username}")
        else:
            # Check if the stock exists in the company table
            cursor.execute("SELECT * FROM company WHERE comp_name = %s", (comp_name,))
            company_data = cursor.fetchall()

            if company_data:  # If the stock exists in company, add it to the watchlist for this user
                if username:
                    # Assuming company_data contains the required columns from the company table
                    cursor.execute('''
                        INSERT INTO portfolio (name, buy_price, curr_price, Quantity, m_name)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (company_data[0][0], company_data[0][2], company_data[0][2], quant, username))
                    connection.commit()
                    return True
                else:
                    print(f"User {username} does not exist.")
                    return False
            else:
                return False
    except mysql.connector.Error as error:
        print("Error:", error)
        
def remove_from_portfolio(comp_name, username):
    try:
        # Check if the stock exists in the portfolio table for the specific user
        cursor.execute("SELECT * FROM portfolio WHERE name = %s AND m_name = %s", (comp_name, username))
        stock_data = cursor.fetchall()

        if stock_data:  # If the stock exists in the portfolio for this user, remove it
            
            cursor.execute("DELETE FROM portfolio WHERE name = %s AND m_name = %s", (comp_name, username))
            connection.commit()
            return True
        
        else:
            return False
    except mysql.connector.Error as error:
        print("Error:", error)
        return False
    

    




def call_sql_function():
    cursor.callproc("update_curr_price")  # Call the SQL procedure
    connection.commit()
    







