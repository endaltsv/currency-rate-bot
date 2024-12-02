import aiohttp
import asyncio

async def fetch_symbol_price(session, symbol):
    url = f'https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}'
    try:
        async with session.get(url) as response:
            data = await response.json()
            if data['retCode'] == 0 and data['result']['list']:
                ticker_data = data['result']['list'][0]
                return float(ticker_data['lastPrice'])
            else:
                print(f"Ошибка при получении данных для {symbol}: {data.get('retMsg', 'Нет данных')}")
                return 0
    except Exception as e:
        print(f"Ошибка при получении данных для {symbol}: {e}")
        return 0

async def fetch_exchange_rates():
    usd_rate = eur_rate = try_rate = 0
    btc_price = eth_price = ton_price = 0

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://api.exchangerate-api.com/v4/latest/RUB') as response:
                currency_data = await response.json()
                usd_rate = 1 / currency_data['rates']['USD']
                eur_rate = 1 / currency_data['rates']['EUR']
                try_rate = 1 / currency_data['rates']['TRY']
        except Exception as e:
            print(f"Ошибка при получении курсов валют: {e}")

        symbols = ['BTCUSDT', 'ETHUSDT', 'TONUSDT']
        tasks = [fetch_symbol_price(session, symbol) for symbol in symbols]
        prices = await asyncio.gather(*tasks)

        btc_price, eth_price, ton_price = prices

    rates = {
        'usd_rate': usd_rate,
        'eur_rate': eur_rate,
        'try_rate': try_rate,
        'btc_price': btc_price,
        'eth_price': eth_price,
        'ton_price': ton_price,
    }

    return rates
