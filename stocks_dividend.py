import requests
from twilio.rest import Client
import pandas as pd
import os
demo = os.getenv("KEY")
tickers = requests.get(f'https://fmpcloud.io/api/v3/symbol/available-nasdaq?apikey={demo}')
tickers = tickers.json()
#print(tickers)
symbols = []
for ticker in tickers:
    symbols.append(ticker['symbol'])
#print(len(symbols))
new_symbols = symbols[0:20]
#print(new_symbols)
DivYield = {}
for company in new_symbols:
  try:
    companydata = requests.get(f'https://fmpcloud.io/api/v3/profile/{company}?apikey={demo}')
    companydata = companydata.json()
    latest_Annual_Dividend = companydata[0]['lastDiv']
    price = companydata[0]['price']
    market_Capitalization = companydata[0]['mktCap']
    name = companydata[0]['companyName']
    exchange = companydata[0]['exchange']
    dividend_Yield= latest_Annual_Dividend/price
    DivYield[company] = {}
    DivYield[company]['Dividend_Yield'] = dividend_Yield
    DivYield[company]['latest_Price'] = price
    DivYield[company]['latest_Dividend'] = latest_Annual_Dividend
    DivYield[company]['market_Capit_in_M'] = market_Capitalization/1000000
    DivYield[company]['company_Name'] = name
    DivYield[company]['exchange'] = exchange
  except:
    pass
df = pd.DataFrame.from_dict(DivYield,orient="index")
df = df.sort_values(["Dividend_Yield"],ascending=False)
pd.set_option("display.max_columns",None)
print(df)
account_sid = os.getenv("SID")
auth_token = os.getenv("TOKEN")
client = Client(account_sid,auth_token)
message = client.messages.create(
    from_="whatsapp:+14155238886",
    body=f"The Best stock to invest for today is {df['company_Name'][0]}",
    to="whatsapp:"
)
#df.to_csv("Div_yield.csv") gets your data to csv format
