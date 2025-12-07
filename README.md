# S&P 500 Pension Strategy

A data-driven investment strategy to try and optimise the long-term returns of my pension by fitting polynomial to S&P 500.

## Files
- `pension_strategy.py` — Python script with full analysis and simulations  
- `pension_strategy_data.sqlite` — SQLite database storing historical S&P 500 prices  

## How to Run
1. Download both files to the same folder.  
2. Install required packages (if not already installed):
```bash
pip install pandas numpy matplotlib yfinance
```
3. Run the Python script:
```bash
python pension_strategy_model.py
```

## What the Script Does
- Downloads 20 years of historical S&P 500 data.  
- Stores and reads the data from an SQLite database.  
- Fit polynomial model to estimate daily fair value.  
- Simulates two investment strategies:  
  1. Add $5 every day.  
  2. Add $5 every day if price is under model, else roll contribution forward.  
- Compares portfolio performance of both strategies.

## Results
- Shows percentage gain and portfolio value for each strategy.  
- Visualises portfolio growth over time with a plot.  
