import yfinance as yf
import matplotlib.pyplot as plt
import requests
import datetime
import matplotlib

matplotlib.use('TkAgg')


def get_ticker(company_name):
    yfinance_url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}
    #
    res = requests.get(url=yfinance_url, params=params, headers={'User-Agent': user_agent})
    data = res.json()
    #
    company_code = data['quotes'][0]['symbol']
    return company_code


def stock_chart(company,ma_window=14):
    comp_ticker = get_ticker(company)
    today = datetime.date.today()
    comp_df = yf.download(comp_ticker, start="2010-01-01", end=today.strftime("%Y-%m-%d"))
    comp_df['MA'] = comp_df['Close'].rolling(window=ma_window).mean()
    # 
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(comp_df.index, comp_df['Close'], label="Closing Price", color='blue')
    ax.plot(comp_df.index, comp_df['MA'], label=f"{ma_window}-Day Moving Average", color='orange')
    ax.set_title(f"Closing Price with {ma_window}-Day Moving Average")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()

    return fig


