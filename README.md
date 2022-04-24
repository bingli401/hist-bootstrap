# hist-bootstrap
clone the repository to your local repo

Make sure you installed python packages: os, getpass, argparse, logging, numpy, pandas, datetime, yfinance.

modify input file: portfolio_input.txt

input any number of securities (tickers)
if it's in foreign currency, make sure to enter the fx ticker (e.g., USDCAD's ticker is CAD=X in yahoo finance).
open a terminal / bash / cmd line

run : Your Python Directory\python.exe "Your Program Directory\main.py" --portfolio portfolio_input.txt

Note: there are other parameters you can input. their default values: --valdate 2022-03-31 --startdate 2017-01-01 --enddate 2022-01-01 --balance 1000000000 --numsim 5000 --conflvl 0.99

output will be in log file and console.
