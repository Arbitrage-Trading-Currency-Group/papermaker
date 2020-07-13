from datetime import datetime
import alpaca_trade_api as tradeapi
from openpyxl import Workbook, load_workbook
# https://realpython.com/python-send-email/
api = tradeapi.REST()
structure = [["", "", "", "", ""], ["Date", datetime.now().strftime("%A"), datetime.now().strftime("%Y-%m-%d"), 'Time:', datetime.now().strftime("%H:%M")], ['Stock', 'IdealQuant', 'AlpacaVol', 'NowPrice', 'Value']]
portfolio = [['ZM', 10, 0, 0, 0], ['FLIR', 250, 0, 0, 0], ['FVRR', 200, 0, 0, 0], ['Z', 3, 0, 0, 0], ['GLD', 12, 0, 0, 0], ['TMO', 32, 0, 0, 0], ['GILD', 20, 0, 0, 0],
             ['PPLT', 370, 0, 0, 0], ['NCR', 50, 0, 0, 0], ['USO', 14, 0, 0, 0], ['DGX', 10, 0, 0, 0], ['SLV', 24, 0, 0, 0], ['LUV', 1, 0, 0, 0],
             ['KTOS', 10, 0, 0, 0], ['ADT', 100, 0, 0, 0], ['HD', 10, 0, 0, 0], ['URI', 10, 0, 0, 0], ['AMZN', 2, 0, 0, 0], ['CCL', 200, 0, 0, 0], ['FB', 10, 0, 0, 0]]
sumPortfolio = [['Total', 8770.93, 0, 1, 8770.93]]


def curr_price(stock):
    barset = api.get_barset(stock, 'day', limit=1)
    bars = barset[stock]
    return bars[0].c


def report_wouldbe():
    workbook = load_workbook(filename="reporting.xlsx")
    sheet = workbook.active
    for index in structure:
        sheet.append(index)
    for index in range(0, len(portfolio), 1):
        portfolio[index][3] = curr_price(portfolio[index][0])
        portfolio[index][4] = portfolio[index][3] * portfolio[index][1]
        sumPortfolio[0][4] += portfolio[index][4]
        # print(portfolio[index])
        sheet.append(portfolio[index])
    print("Current Would-Be Value: " + str(round(sumPortfolio[0][4], 2)))
    sheet.append(sumPortfolio[0])
    workbook.save(filename="reporting.xlsx")


def update_positions():
    for stock in portfolio:
        stock[2] = api.get_position(stock[0]).qty


def check_if_open():
    # Check if the market is open now.
    clock = api.get_clock()
    print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
    return clock.is_open

# def pull_change(ticker, ranger):
#     # Get daily price data for Stock over the last 5 trading days.
#     barset = api.get_barset(ticker, 'day', limit=5)
#     ticker_bars = barset[ticker]
#     # See how much Stock moved in that timeframe.
#     start = ticker_bars[3 - ranger].c
#     stop = ticker_bars[-1].c
#     close_price = ticker_bars[-1]
#     percent_change = round((stop - start) / start * 100, 2)
#     print('In ' + str(ranger) + ' days, ' + ticker + ' moved {}%'.format(percent_change))
#     print('Close Price ' + str(close_price))
#     return close_price

# Scan for changes over variable period
# if check_if_open():
# for stock in portfolio:
#     pull_change(stock, 1)


def todays_change(ticker):
    # Get daily price data for Stock over the last 5 trading days.
    barset = api.get_barset(ticker, 'day', limit=5)
    ticker_bars = barset[ticker]
    # See how much Stock moved in that timeframe.
    start = ticker_bars[3].c
    stop = ticker_bars[4].c
    percent_change = round((stop - start) / start * 100, 2)
    # print('Today, ' + ticker + ' moved {}%'.format(percent_change))
    return percent_change


def submit_order(symbol, qty, side, typeo):
    # Submit a market order to buy 1 share of Apple at market price
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=typeo,
        time_in_force='gtc'
    )


def main():
    report_wouldbe()
    if check_if_open():
        update_positions()
        for stock in portfolio:
            print('Today, '+ stock[0] + ' moved ' + str(todays_change(stock[0])) + '%')
            if todays_change(stock[0]) >= 3:
                if int(stock[2])-1 > 0:
                    submit_order(stock[0], int(stock[2])-1, 'sell', 'market')
                    print(str(stock[0]) + ' has increased by ' + str(todays_change(stock[0])) + '% Sell of ' + str(int(stock[2])-1) + ' has been issued.')
                else:
                    print('No volume of ' + str(stock[0]) + ' to sell')
            elif todays_change(stock[0]) <= -3:
                if int(stock[2]) < stock[1] * 3:
                    submit_order(stock[0], stock[1], 'buy', 'market')
                    print(stock[0] + ' has decreased by ' + str(todays_change(stock[0])) + '% Buy of ' + str(stock[1]) + ' has been issued.')
                else:
                    print('No Action Taken on' + str(stock[0]))

main()


