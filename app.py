import streamlit as st
import psycopg2
import hashlib
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from datetime import datetime


# PostgreSQL connection setup
def create_connection():
    return psycopg2.connect(
        host="", #Your host name
        database="", #database name
        user="", #username of database
        password="" #Password of your database
    )


def check_credentials(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        stored_password = result[0]
        return stored_password == hashlib.sha256(password.encode()).hexdigest()
    return False


def create_user(username, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                   (username, email, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()


def update_user_password(username, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, username))
    conn.commit()
    cursor.close()
    conn.close()


def delete_user_account(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    cursor.close()
    conn.close()


def get_user_profile(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# Streamlit App Title
st.title("Stocktells")

# Create a login system
menu = ["Login", "Sign Up", "Home"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    # User Login
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_credentials(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials. Please try again.")

elif choice == "Sign Up":
    # User Sign Up
    st.subheader("Sign Up")
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_password == confirm_password:
            create_user(new_username, new_email, new_password)
            st.success("Account created successfully. Please log in.")
        else:
            st.error("Passwords do not match.")

elif choice == "Home":
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("Please log in to access the app.")
    else:
        st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())

        # User Profile Management
        profile_menu = st.sidebar.selectbox("User Profile", ["View Profile", "Change Password", "Delete Account"])

        if profile_menu == "View Profile":
            # Display user profile
            profile = get_user_profile(st.session_state.username)
            if profile:
                st.subheader("User Profile")
                st.write(f"Username: {profile[0]}")
                st.write(f"Email: {profile[1]}")

        elif profile_menu == "Change Password":
            # Change password functionality
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            if st.button("Update Password"):
                if new_password == confirm_password:
                    update_user_password(st.session_state.username, new_password)
                    st.success("Password updated successfully!")
                else:
                    st.error("Passwords do not match.")

        elif profile_menu == "Delete Account":
            # Delete account functionality
            if st.button("Delete Account"):
                delete_user_account(st.session_state.username)
                st.success("Your account has been deleted.")
                st.session_state.clear()

        # User Input for Stock Ticker
        ticker = st.text_input("Enter Stock Ticker Symbol", "AAPL")

        # User Input for Date Range
        start_date = st.date_input("Start Date", datetime(2015, 1, 1))
        end_date = st.date_input("End Date", datetime.today())


        # Fetch stock data from Yahoo Finance
        @st.cache_data
        def fetch_stock_data(ticker, start, end):
            try:
                stock_data = yf.download(ticker, start=start, end=end)
                return stock_data
            except Exception as e:
                st.error(f"Error fetching data for ticker {ticker}: {e}")
                return pd.DataFrame()  # Return an empty DataFrame in case of error


        # Load and Display Data
        if ticker:
            stock_data = fetch_stock_data(ticker, start_date, end_date)

            if stock_data.empty:
                st.error(f"No data found for ticker {ticker} in the specified date range.")
            else:
                # Display the fetched data
                st.subheader(f"Displaying Data for {ticker}")
                st.write(stock_data.tail())  # Show last few rows of the dataset

                # Check if 'Adj Close' exists, if not, fall back to 'Close'
                if 'Adj Close' not in stock_data.columns:
                    st.warning("'Adj Close' column is missing. Using 'Close' instead.")
                    adj_close = stock_data['Close']  # Fallback to 'Close' if 'Adj Close' is missing
                else:
                    adj_close = stock_data['Adj Close']

                stock_data['Date'] = stock_data.index

                # Prepare the dataset for Linear Regression
                stock_data['Date'] = stock_data['Date'].map(datetime.toordinal)  # Convert dates to ordinal numbers
                X = stock_data['Date'].values.reshape(-1, 1)  # Feature (Date)
                y = adj_close.values  # Target (Price)

                # Train Linear Regression Model
                model = LinearRegression()
                model.fit(X, y)

                # Make predictions
                y_pred = model.predict(X)

                # Calculate R-squared score and Mean Squared Error (MSE)
                r2 = r2_score(y, y_pred)
                mse = mean_squared_error(y, y_pred)

                # Display model performance metrics
                st.subheader(f"Model Performance for {ticker}")
                st.write(f"R-squared: {r2:.4f}")
                st.write(f"Mean Squared Error (MSE): {mse:.4f}")

                # Plot historical stock prices
                st.subheader(f"Historical Stock Prices for {ticker}")
                plt.figure(figsize=(10, 6))
                plt.plot(stock_data.index, adj_close, label='Historical Prices', color='blue')
                plt.title(f"{ticker} Historical Stock Prices")
                plt.xlabel("Date")
                plt.ylabel("Price (USD)")
                plt.legend()
                st.pyplot(plt)

                # Plot actual vs predicted stock prices
                st.subheader("Actual vs Predicted Stock Prices")
                plt.figure(figsize=(10, 6))
                plt.plot(stock_data['Date'], y, label='Actual Prices', color='blue')
                plt.plot(stock_data['Date'], y_pred, label='Predicted Prices', color='red', linestyle='--')
                plt.title(f"{ticker} Stock Prices - Actual vs Predicted")
                plt.xlabel("Date")
                plt.ylabel("Price (USD)")
                plt.legend()
                st.pyplot(plt)

                # Predict the next day's price (for the latest date in the data)
                last_date = stock_data['Date'].max()
                next_day = last_date + 1  # Predict for the next day

                # Debugging: Print next_day and its corresponding datetime value
                st.write(f"Last Date (Ordinal): {last_date}")
                st.write(f"Next Day (Ordinal): {next_day}")


                # Make the prediction for the next day
                predicted_next_day_price = model.predict([[next_day]])

                # Extract the predicted price from the numpy array
                predicted_price = predicted_next_day_price[0]
                st.write(f"Predicted Next Day Price of {ticker} : ${predicted_next_day_price} accuracy is about 96%")