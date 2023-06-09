#################
#####  FIB  #####
#################

def ro(num):
    if num is None:
        return 0

    return round(num, 2)


def fib_retracement(p1, p2):
    list =[0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236]
    dict = {}
    dist = p2 - p1
    for val in list:
        dict[str(val) ] =  "%.2f" % (p2 - dist*val)
    return dict
#Fibonacci Retracement ends here

def fib (data):
    #Calculate the max and min close price
    maximum_price = data['Close'].max()
    minimum_price = data['Close'].min()
    return fib_retracement ( maximum_price, minimum_price )

# https://github.com/sanampatel/python-pivot-levels/blob/master/pivot_levels.py #
def classic(opens, high, low, close):
    pivot = dict()
    ran = ro(high - low)
    pivot["PP"] = ro((high + low + close) / 3)

    pivot["R1"] = ro((pivot["PP"] * 2) - low)
    pivot["R2"] = ro(pivot["PP"] + ran)
    pivot["R3"] = ro(pivot["R2"] + ran)  # pivot["PP"] + (ran * 2)
    pivot["R4"] = ro(pivot["R3"] + ran)   # pivot["PP"] + (ran * 3)

    pivot["S1"] = ro((pivot["PP"] * 2) - high)
    pivot["S2"] = ro(pivot["PP"] - ran)
    pivot["S3"] = ro(pivot["S2"] - ran)
    pivot["S4"] = ro(pivot["S3"] - ran)

    return pivot


def fibonacci(opens, high, low, close):
    pivot = dict()
    pivot["PP"] = ro((high + low + close) / 3)

    pivot["R1"] = ro(pivot["PP"] + ((high - low) * .382))
    pivot["R2"] = ro(pivot["PP"] + ((high - low) * .618))
    pivot["R3"] = ro(pivot["PP"] + ((high - low) * 1.000))

    pivot["S1"] = ro(pivot["PP"] - ((high - low) * .382))
    pivot["S2"] = ro(pivot["PP"] - ((high - low) * .618))
    pivot["S3"] = ro(pivot["PP"] - ((high - low) * 1.000))

    return pivot


def woodie(opens, high, low, close):
    pivot = dict()
    ran = ro(high - low)
    pivot["PP"] = ro((high + low + close) / 3)

    pivot["PP"] = ro((high + low + (opens * 2)) / 4)

    pivot["R1"] = ro((pivot["PP"] * 2) - low)
    pivot["R2"] = ro(pivot["PP"] + ran)
    pivot["R3"] = ro(pivot["R1"] + ran)
    pivot["R4"] = ro(pivot["R3"] + ran)

    pivot["S1"] = ro((pivot["PP"] * 2) - high)
    pivot["S2"] = ro(pivot["PP"] - ran)
    pivot["S3"] = ro(pivot["S1"] - ran)
    pivot["S4"] = ro(pivot["S3"] - ran)

    return pivot

def camarilla(opens, high, low, close):
    pivot = dict()
    ran = ro(high - low)

    pivot["PP"] = ro((high + low + close) / 3)

    pivot["R1"] = ro(close + (ran * 1.1/12))
    pivot["R2"] = ro(close + (ran * 1.1/6))
    pivot["R3"] = ro(close + (ran * 1.1/4))
    pivot["R4"] = ro(close + (ran * 1.1/2))

    pivot["S1"] = ro(close - (ran * 1.1/12))
    pivot["S2"] = ro(close - (ran * 1.1/6))
    pivot["S3"] = ro(close - (ran * 1.1/4))
    pivot["S4"] = ro(close - (ran * 1.1/2))

    return pivot

def demark(opens, high, low, close):
    pivot = dict()
    factor = 0

    if close < opens:
        factor = (high + (low * 2) + close)

    if close > opens:
        factor = ((high * 2) + low + close)

    if close == opens:
        factor = (high + low + (close * 2))

    pivot["PP"] = ro(factor / 4)
    pivot["R1"] = ro(factor / 2 - low)
    pivot["S1"] = ro(factor / 2 - high)

    return pivot


# https://github.com/sanampatel/python-pivot-levels/blob/master/pivot_levels.py #
def pivot_levels(opens, high, low, close):
    pivot = dict()
    pivot["pivot"] = dict()

    #pivot["input"] = {"open": opens, "high": high, "low": low, "close": close}
    #pivot["pivot"]["classic"] = classic(opens, high, low, close)
    #pivot["pivot"]["fibonacci"] = fibonacci(opens, high, low, close)
    #pivot["pivot"]["woodie"] = woodie(opens, high, low, close)
    pivot["pivot"]["camarilla"] = camarilla(opens, high, low, close)
    #pivot["pivot"]["demark"] = demark(opens, high, low, close)

    return pivot
