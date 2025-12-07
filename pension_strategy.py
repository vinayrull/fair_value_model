import sqlite3
import yfinance as yf
from datetime import date, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% import data

con = sqlite3.connect('pension_strategy_data.sqlite')
cur = con.cursor()

two_decade = date.today() - timedelta(days=365*20)
sp500 = yf.download("^GSPC", start=two_decade)

cur.executescript("""
    DROP TABLE IF EXISTS Historical_Price;
    CREATE TABLE Historical_Price (
        date TEXT PRIMARY KEY,
        price FLOAT
        )
    """)

for idx, rows in sp500.iterrows():
    cur.execute("""
    INSERT INTO Historical_Price (date, price)
    VALUES (?, ?) """, (idx.strftime("%Y-%m-%d"), float(rows["Close"])))

df = pd.read_sql("""
                 SELECT *
                 FROM Historical_Price
                 ORDER BY date ASC
                 """, con, parse_dates=["date"])    

df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
full_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")
df = df.reindex(full_range)
df["price"] = df["price"].ffill()
df = df.reset_index().rename(columns={"index": "date"})           
     
con.commit()
cur.close()
con.close()

#%% model analysis
# Test 1 - add £5 every day
# Test 2 - add £5 every day if price is under model, else add to next day contribution

test1_price = list()
test2_price = list()
test1_units = list()
test2_units = list()
cash_buffer = 0 
total_invested = 0 
look_back = len(df) // 2

for i in range(look_back, len(df)):
    df_hist = df.iloc[i - look_back: i]
    row = df.iloc[i]

    # model for each day
    x = np.arange(len(df_hist))
    y = df_hist["price"].values
    coeffs = np.polyfit(x, y,2)
    model = np.poly1d(coeffs)    
    x_day = len(df_hist)
    model_price = model(x_day)
    price = row["price"]
    
    # test 1
    unit = 5 / price
    test1_units.append(unit)
    test1_price.append(sum(test1_units) * price)
    
    # test 2
    if  price > model_price:
        cash_buffer += 5
        test2_units.append(0)
        test2_price.append(sum(test2_units) * price)
    else:
        invested_amount = 5 + cash_buffer
        units_bought = invested_amount / price
        test2_units.append(units_bought)
        cash_buffer = 0 
        test2_price.append(sum(test2_units) * price)
    
    total_invested += 5

final_price = df["price"].iloc[-1]
final_value1 = final_price * sum(test1_units) 
final_value2 = (final_price * sum(test2_units)) + cash_buffer
total_return1 = (final_value1 - total_invested) / total_invested
total_return2 = (final_value2 - total_invested) / total_invested

print("Test 1 - Add £5 at start of every day")
print(f"Percentage gain is {round(total_return1*100,2)}% current value is ${round(final_value1)}")
print("Test 2 - Add £5 at start of every day if price is under model, else add to next day contribution")
print(f"Percentage gain is {round(total_return2*100,2)}% current value is ${round(final_value2)}")

#%% compare return of both tests

dates_for_test = df["date"].iloc[look_back:].reset_index(drop=True)
plt.figure(figsize=(12,6))
plt.plot(dates_for_test, test1_price, label="Automation", linewidth=2)
plt.plot(dates_for_test, test2_price, label="Market Timing", linewidth=2)
plt.ylabel("Portfolio Value ($)")
plt.xlabel("Date")
plt.title("Automation VS Market Timing", fontsize=25)
plt.legend()
plt.show()