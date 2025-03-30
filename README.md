# Stocktells - Stock Price Prediction and User Authentication
Welcome to Stocktells, a stock price prediction app built with Streamlit, PostgreSQL, and Machine Learning techniques. This app allows users to log in, sign up, manage their profiles, and predict stock prices based on historical data.

# Features:
User Authentication: Users can sign up, log in, change passwords, and delete their accounts.

Stock Price Prediction: Uses a simple Linear Regression model to predict future stock prices based on historical data.

Data Visualization: Displays historical stock prices and compares actual vs predicted values.

PostgreSQL Database: Securely stores user credentials and profile data.

# Requirements:
Python 3.x

Streamlit

psycopg2 (PostgreSQL driver)

yfinance (Yahoo Finance data)

scikit-learn (Machine Learning)

matplotlib (Plotting)

# Setup Instructions:
# 1. Install Dependencies:
To install the necessary libraries, run the following command:


pip install streamlit psycopg2 yfinance scikit-learn matplotlib
# 2. PostgreSQL Setup:
This app uses PostgreSQL to store user data, including usernames, emails, and hashed passwords. You need to:

Set up a PostgreSQL database with a table named users containing columns: username, email, and password.

Adjust the PostgreSQL connection in the create_connection() function to match your own database credentials.


def create_connection():
    return psycopg2.connect(
        host="your_host",  # Your PostgreSQL host
        database="your_db",  # Your database name
        user="your_user",  # Your PostgreSQL username
        password="your_password"  # Your PostgreSQL password
    )
# 3. Running the App:
Once the dependencies are installed and your database is set up, you can run the app with:


streamlit run app.py
This will start the Streamlit app locally. Navigate to the URL provided by Streamlit in your browser to interact with the app.

# 4. Key Features:

User Authentication:
Login: Enter your username and password to log in.

Sign Up: Create a new user account with a username, email, and password.

Profile Management: After logging in, you can:

View your profile (username and email).

Change your password.

Delete your account.

Stock Price Prediction:
Enter Ticker: Input a stock ticker symbol (e.g., "AAPL" for Apple).

Date Range: Specify the start and end dates for historical data.

Stock Data Fetching: Fetch stock data from Yahoo Finance using yfinance.

Linear Regression Model: Predict the stock price for the next day using a simple linear regression model.

Visualizations: View historical stock prices and actual vs predicted stock prices.

5. How it Works:
Stock Data: The app fetches historical stock data for the specified ticker symbol from Yahoo Finance.

Prediction: A linear regression model is used to predict the next day's price based on historical data.

Performance Metrics: The app displays the model's R-squared score and Mean Squared Error (MSE).

Plots: Historical prices and the prediction model are visualized using matplotlib.

6. Code Breakdown:
User Authentication: The app handles user login, signup, and profile management with password hashing using SHA256.

Stock Price Prediction: The app uses yfinance to download stock data and scikit-learn’s LinearRegression to make predictions.

PostgreSQL Integration: User data is securely stored and managed in a PostgreSQL database.

7. Example Workflow:
Sign Up: Create a new account with a username and password.

Login: Log into your account with the credentials you just created.

Stock Prediction:

Input a stock ticker like AAPL (Apple Inc.).

Choose a date range for historical data.

View the historical stock data and the model’s predictions for the next day.

8. Screenshots:
Login Screen: ![Screenshot 2025-03-18 144558](https://github.com/user-attachments/assets/7f051e58-d991-42cc-be96-bcf06b0c7aac)


Stock Prediction: ![Screenshot 2025-03-18 144709](https://github.com/user-attachments/assets/e1920f44-a5c7-48bb-94a2-7dac1d801eb2)

![Screenshot 2025-03-18 144731](https://github.com/user-attachments/assets/24bb33d0-6920-4aaa-af41-5056002ed553)

![Screenshot 2025-03-18 144752](https://github.com/user-attachments/assets/68e94472-9a69-46ca-b7fb-898014eebad7)

![Screenshot 2025-03-18 144807](https://github.com/user-attachments/assets/bb17e89d-f458-4879-89d2-e42700c5ca9f)

![Screenshot 2025-03-18 144823](https://github.com/user-attachments/assets/06e2a134-f077-4121-a33b-569105e64d03)

