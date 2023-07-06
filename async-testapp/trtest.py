import requests, json, time, datetime


def mlog(market, *text):
    text = [str(i) for i in text]
    text = " ".join(text)

    datestamp = str(datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3])

    print("[{} {}] - {}".format(datestamp, market, text))


def get_symbols(screener_country):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://scanner.tradingview.com/{}/scan".format(screener_country)
    symbol_lists = requests.post(url, headers=headers).json()
    data = symbol_lists["data"]
    return data


def get_signal(screener_country, market_symbol, symbol, candle):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://scanner.tradingview.com/{}/scan".format(screener_country)

    payload = {
        "symbols": {
            "tickers": ["{}:{}".format(market_symbol, symbol)],
            "query": {"types": []},
        },
        "columns": [
            "Recommend.Other|{}".format(candle),
            "Recommend.All|{}".format(candle),
            "Recommend.MA|{}".format(candle),
            "RSI|{}".format(candle),
            "RSI[1]|{}".format(candle),
            "Stoch.K|{}".format(candle),
            "Stoch.D|{}".format(candle),
            "Stoch.K[1]|{}".format(candle),
            "Stoch.D[1]|{}".format(candle),
            "CCI20|{}".format(candle),
            "CCI20[1]|{}".format(candle),
            "ADX|{}".format(candle),
            "ADX+DI|{}".format(candle),
            "ADX-DI|{}".format(candle),
            "ADX+DI[1]|{}".format(candle),
            "ADX-DI[1]|{}".format(candle),
            "AO|{}".format(candle),
            "AO[1]|{}".format(candle),
            "Mom|{}".format(candle),
            "Mom[1]|{}".format(candle),
            "MACD.macd|{}".format(candle),
            "MACD.signal|{}".format(candle),
            "Rec.Stoch.RSI|{}".format(candle),
            "Stoch.RSI.K|{}".format(candle),
            "Rec.WR|{}".format(candle),
            "W.R|{}".format(candle),
            "Rec.BBPower|{}".format(candle),
            "BBPower|{}".format(candle),
            "Rec.UO|{}".format(candle),
            "UO|{}".format(candle),
            "EMA10|{}".format(candle),
            "close|{}".format(candle),
            "SMA10|{}".format(candle),
            "EMA20|{}".format(candle),
            "SMA20|{}".format(candle),
            "EMA30|{}".format(candle),
            "SMA30|{}".format(candle),
            "EMA50|{}".format(candle),
            "SMA50|{}".format(candle),
            "EMA100|{}".format(candle),
            "SMA100|{}".format(candle),
            "EMA200|{}".format(candle),
            "SMA200|{}".format(candle),
            "Rec.Ichimoku|{}".format(candle),
            "Ichimoku.BLine|{}".format(candle),
            "Rec.VWMA|{}".format(candle),
            "VWMA|{}".format(candle),
            "Rec.HullMA9|{}".format(candle),
            "HullMA9|{}".format(candle),
            "Pivot.M.Classic.S3|{}".format(candle),
            "Pivot.M.Classic.S2|{}".format(candle),
            "Pivot.M.Classic.S1|{}".format(candle),
            "Pivot.M.Classic.Middle|{}".format(candle),
            "Pivot.M.Classic.R1|{}".format(candle),
            "Pivot.M.Classic.R2|{}".format(candle),
            "Pivot.M.Classic.R3|{}".format(candle),
            "Pivot.M.Fibonacci.S3|{}".format(candle),
            "Pivot.M.Fibonacci.S2|{}".format(candle),
            "Pivot.M.Fibonacci.S1|{}".format(candle),
            "Pivot.M.Fibonacci.Middle|{}".format(candle),
            "Pivot.M.Fibonacci.R1|{}".format(candle),
            "Pivot.M.Fibonacci.R2|{}".format(candle),
            "Pivot.M.Fibonacci.R3|{}".format(candle),
            "Pivot.M.Camarilla.S3|{}".format(candle),
            "Pivot.M.Camarilla.S2|{}".format(candle),
            "Pivot.M.Camarilla.S1|{}".format(candle),
            "Pivot.M.Camarilla.Middle|{}".format(candle),
            "Pivot.M.Camarilla.R1|{}".format(candle),
            "Pivot.M.Camarilla.R2|{}".format(candle),
            "Pivot.M.Camarilla.R3|{}".format(candle),
            "Pivot.M.Woodie.S3|{}".format(candle),
            "Pivot.M.Woodie.S2|{}".format(candle),
            "Pivot.M.Woodie.S1|{}".format(candle),
            "Pivot.M.Woodie.Middle|{}".format(candle),
            "Pivot.M.Woodie.R1|{}".format(candle),
            "Pivot.M.Woodie.R2|{}".format(candle),
            "Pivot.M.Woodie.R3|{}".format(candle),
            "Pivot.M.Demark.S1|{}".format(candle),
            "Pivot.M.Demark.Middle|{}".format(candle),
            "Pivot.M.Demark.R1|{}".format(candle),
        ],
    }

    resp = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    signal = oscillator = resp["data"][0]["d"][1]

    return signal


# get_signal("BTCUSDT", 60)
# get_signal("turkey","BIST","ERCB", 60)


def isControlStrongSymbols(symbols, screener_country, market_symbol, candle_list):
    signals_list = []
    info = "Buy/Sell Signals from @tradingview - {} min candle\n".format(candle_list)
    print(info)
    while True:
        for symbol in symbols:
            for candle in candle_list:
                signal1 = []
                msg = ""
                print("Symbol :", symbol)
                print("Candle :", candle)
                print("Market Symbol :", market_symbol)
                print("Screener Country :", screener_country)
                break
                signal = round(
                    get_signal(screener_country, market_symbol, symbol, candle), 3
                )
                signal1.append(signal)
                msg += "{} Signal: {} Candle: {} ".format(symbol, signal, candle)
                if signal > 0.5:
                    msg += "STRONG BUY"
                    print("Mesage :", msg)
                elif signal > 0:
                    msg += "BUY"
                    print("Mesage :", msg)
                elif signal > -0.5:
                    msg += "SELL"
                    print("Mesage :", msg)
                    time.sleep(2)
                else:
                    msg += "STRONG SELL"
                    print("Mesage :", msg)
                    time.sleep(2)
                signals_list.append(signal1)
                time.sleep(1)
        print("#####################################################################")


def run(screener_country, candle_list):
    temp = []
    signals_list = []
    data = get_symbols(screener_country)
    for i in data:
        list_symbol = i["s"].split(":")
        market_symbol = list_symbol[0]
        symbol = list_symbol[1]
        for candle in candle_list:
            signal1 = []
            try:
                signal = round(
                    get_signal(screener_country, market_symbol, symbol, candle), 3
                )
                signal1.append(signal)
                if signal > 0.53:
                    msg = "strong buy"
                    signals_list.append(signal1)
                    temp.append(symbol)
                    print("Symbol :", symbol)
                    print("Candle :", candle)
                    print("Market Symbol :", market_symbol)
                    print("Screener Country :", screener_country)
                    msg = "{} {} : {} {} min candle".format(symbol, signal, msg, candle)
                    print("\nMesage :", msg)
                    break
            except:
                print("Analiz verisi alınamadı,hisse :", i)
    return temp


menu_options = {
    1: "Piyasa Verilerini Tara:(Filter~Strong Buy)",
    2: "Hisse Senetlerimi Tara:(Ornek Data Format ERCB,VESBE,CASA,ZRGYO)",
}


def print_menu():
    for key in menu_options.keys():
        print(key, "--", menu_options[key])


if __name__ == "__main__":
    screener_country = "crypto"
    market_symbol = "BINANCE"
    print("*****************~TRADINGVIEW ANALYSIS~*****************")
    print_menu()
    option = int(input("Enter your choice (1 OR 2): "))
    if option == 1:
        print("Hisse Seneti Analiz Periyotları (5,15,30,45,60,240,1W)\n")
        data = input("Analiz Periyodunu Giriniz(Ornek 5,15)=")
        candle_list = data.split(",")
        info = "Turkish Stocks Buy/Sell Signals from @tradingview - {} min candle list\n".format(
            candle_list
        )
        print(info)
        data = run(screener_country, candle_list)
        strongBuySymbols = list(dict.fromkeys(data))
        print("***********************************")
        print("Strong Buy Symbols : ", strongBuySymbols)
        print("*********************************\n")
        candle_list = [5]
        isControlStrongSymbols(
            strongBuySymbols, screener_country, market_symbol, candle_list
        )
    elif option == 2:
        mySembols = input("Hisselerinizi Giriniz: ")
        data = mySembols.split(",")
        print("Hisse Seneti Analiz Periyotları (5,15,30,45,60,240,1W)\n")
        candleData = input("Analiz Periyodunu Giriniz(Ornek 5,15)=")
        candle_list = candleData.split(",")
        isControlStrongSymbols(data, screener_country, market_symbol, candle_list)
    else:
        print("Invalid option. Please enter a number 1 or 2.")

    # online python test url
    # https://trinket.io/embed/python3
    # https://www.programiz.com/python-programming/online-compiler/
