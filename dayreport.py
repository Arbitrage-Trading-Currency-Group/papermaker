import alpaca_trade_api as tradeapi
import self as self

#Run this after close each day or modify to run just after open.
#Export to excel file

api = tradeapi.REST()

portfolio = ['ZM', 'FLIR', 'FVRR', 'Z', 'GLD', 'PPLT', 'NCR', 'USO', 'DGX', 'SLV',
             'LUV', 'KTOS', 'ADT', 'HD', 'URI', 'AMZN', 'CCL', 'FB']


def check_if_open():
    # Check if the market is open now.
    clock = api.get_clock()
    print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
    return clock.is_open


def pull_change(ticker, ranger):
    # Get daily price data for Stock over the last 5 trading days.
    barset = api.get_barset(ticker, 'day', limit=5)
    ticker_bars = barset[ticker]
    # See how much Stock moved in that timeframe.
    start = ticker_bars[3 - ranger].c
    stop = ticker_bars[-1].c
    close_price = ticker_bars[-1]
    percent_change = round((stop - start) / start * 100, 2)
    print('In ' + str(ranger) + ' days, ' + ticker + ' moved {}%'.format(percent_change))
    print('Close Price ' + str(close_price))
    return close_price

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


# def main():
for stock in portfolio:
    print('Today, ' + stock + ' moved ' + str(todays_change(stock)) + '%')
    if todays_change(stock) >= 2:
        # print(stock + 'has increased. Sell to be issued.')
        # submit_order(stock, 10, 'sell', 'market')
        print(stock + ' has increased. Sell has been issued.')
    elif todays_change(stock) <= -2:
        # print(stock + 'has decreased. Buy to be issued.')
        # submit_order(stock, 10, 'buy', 'market')
        print(stock + ' has decreased. Buy has been issued.')
    else:
        print('No Action Taken')




