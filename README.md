# S&P 500 Fair Value Model

A data-driven investment strategy to optimize long-term returns by modeling the daily fair value of the S&P 500 using polynomial regression.

## Files
- `fair_value_model.py` — Python script with full analysis and simulations  
- `fair_value_data.sqlite` — SQLite database storing historical S&P 500 prices  

## How to Run
1. Download both files to the same folder.  
2. Install required packages (if not already installed):
```bash
pip install pandas numpy matplotlib yfinance
```
3. Run the Python script:
```bash
python fair_value_model.py
```

## What the Script Does
- Downloads 20 years of historical S&P 500 data.  
- Stores and reads the data from an SQLite database.  
- Builds a polynomial regression model to estimate daily fair value.  
- Simulates two investment strategies:  
  1. Add $5 every day.  
  2. Add $5 every day if price is under model, else roll contribution forward.  
- Compares portfolio performance of both strategies.

## Results
- Shows percentage gain and portfolio value for each strategy.  
- Visualizes portfolio growth over time with a plot.  

## Key Techniques
- Polynomial regression modeling  
- SQLite database management  
- Time series analysis  
- Investment strategy simulation
