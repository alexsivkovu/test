import json

RAW_DEFAULT = r"raw.chartblock.json"
CASH_DEFAULT = 1.0


def strategy(raw: str = RAW_DEFAULT,
             cash: float = CASH_DEFAULT) -> float:
    """Calculates the maximum profit of the trading

    :param raw: path to raw json file
    :param cash: initial money capital in USD
    :return: net profit (overall fortune - cash) or Exception, if input data is invalid
    """

    with open(raw, 'r') as file:
        data = json.load(file)

    # declare bids & asks
    for elem in data:
        if elem['name'] == 'bid':
            bids = elem['ticks']
        if elem['name'] == 'ask':
            asks = elem['ticks']

    if not ('bids' in locals()) & ('asks' in locals()):
        raise NameError('Invalid raw data')

    # initialize temp variables
    fortune = cash  # here we will accumulate the money
    ask_first = asks[0][1]  # the initial ask

    for ask, bid in zip(asks, bids):
        # check that sell now and buy next tick is profitable
        if cash // ask_first * bid[1] + cash % ask_first - fortune > 0:
            # if True, sell & buy -> increase the total fortune
            fortune = cash // ask_first * bid[1] + cash % ask_first
        # if ask decreased, we re-initialize ask_first
        if ask[1] < ask_first:
            ask_first = ask[1]

    return fortune - cash


if __name__ == '__main__':
    print(strategy())
