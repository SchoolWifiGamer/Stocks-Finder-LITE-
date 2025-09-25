import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta


def get_stock_data(symbol, period='1mo'):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)

        if hist.empty:
            return None

        info = stock.info

        current_price = hist['Close'][-1]
        previous_price = hist['Close'][0]
        change = current_price - previous_price
        change_percent = (change / previous_price) * 100

        # Made by Gao Le
        volume = hist['Volume'].mean()
        high_52wk = info.get('fiftyTwoWeekHigh', current_price)
        low_52wk = info.get('fiftyTwoWeekLow', current_price)

        return {
            'symbol': symbol,
            'current_price': current_price,
            'change': change,
            'change_percent': change_percent,
            'company_name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'volume': volume,
            'high_52wk': high_52wk,
            'low_52wk': low_52wk,
            'history': hist
        }
    except Exception as e:
        print(f"Error processing {symbol}: {e}")
        return None


def plot_stock_data(hist, symbol, company_name):
    plt.figure(figsize=(12, 6))
    plt.plot(hist.index, hist['Close'], linewidth=2)
    plt.title(f'{symbol} - {company_name} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_multiple_stocks(symbols_data):
    plt.figure(figsize=(14, 8))

    for data in symbols_data:
        if data and not data['history'].empty:
            
            normalized = (data['history']['Close'] /
                          data['history']['Close'].iloc[0]) * 100
            plt.plot(data['history'].index, normalized,
                     label=data['symbol'], linewidth=2)

    plt.title('Stock Performance Comparison (Normalized)')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def display_stock_info(data):
    if not data:
        return

    print(f"\n{'='*60}")
    print(f"{data['symbol']} - {data['company_name']}")
    print(f"{'='*60}")
    print(f"Current Price: ${data['current_price']:.2f}")
    print(f"Change: ${data['change']:+.2f} ({data['change_percent']:+.2f}%)")
    print(f"Sector: {data['sector']}")
    print(f"Market Cap: ${data['market_cap']:,.0f}" if data['market_cap']
          != 'N/A' else "Market Cap: N/A")
    print(f"52-Week High: ${data['high_52wk']:.2f}")
    print(f"52-Week Low: ${data['low_52wk']:.2f}")
    print(f"Average Volume: {data['volume']:,.0f}")


def infinite_stock_analyzer():
    print("=== INFINITE STOCK ANALYZER ===")
    print("Enter stock symbols one by one")
    print("Type 'done' when finished, 'quit' to exit\n")

    symbols = []
    all_data = []

    while True:
        symbol = input("Enter stock symbol: ").strip().upper()

        if symbol == 'QUIT':
            return
        elif symbol == 'DONE':
            break
        elif symbol == '':
            continue
        elif symbol in symbols:
            print(f"✓ {symbol} already in list")
            continue

        
        if len(symbol) < 1 or len(symbol) > 5:
            print("Invalid symbol format")
            continue

        symbols.append(symbol)
        print(f"✓ Added {symbol} (Total: {len(symbols)} symbols)")

    if not symbols:
        print("No symbols to analyze.")
        return

    print(f"\n📊 Analyzing {len(symbols)} stocks...")

    for symbol in symbols:
        data = get_stock_data(symbol)
        if data:
            all_data.append(data)
            display_stock_info(data)

            if input(f"\nPlot chart for {symbol}? (y/n): ").lower() == 'y':
                plot_stock_data(data['history'], symbol, data['company_name'])
        else:
            print(f"❌ Could not fetch data for {symbol}")

    if len(all_data) > 1:
        compare = input(
            f"\nCompare all {len(all_data)} stocks on one chart? (y/n): ").lower()
        if compare == 'y':
            plot_multiple_stocks(all_data)

    
    print(f"\n🎯 Analysis Complete!")
    print(
        f"Successfully analyzed {len(all_data)} out of {len(symbols)} stocks")



if __name__ == "__main__":
    infinite_stock_analyzer()
