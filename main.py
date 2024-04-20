import platform
import aiohttp
import asyncio
from datetime import datetime,timedelta
import pandas as pd

# async def treatment(data):
#     list = request(data)
#     return await asyncio.gather(list)

async def request(data, *args):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={data}') as response:
            list = await response.json()
            if "exchangeRate" in list:
                list = list["exchangeRate"]
                list_dict = {}
                for dict in list:
                    for key, value in dict.items():
                        if key=="currency" and value=="EUR"or key=="currency" and value=="USD": 
                            list_dict[f"{value}"] ={'saleRate':dict['saleRate'], 'purchaseRate':dict['purchaseRate']}
    return (f"{data}:{list_dict}")

async def main(day, *args):
    start_date = datetime.now()
    end_date = start_date - timedelta(days=day-1)
    r = pd.date_range(
    min(start_date, end_date),
    max(start_date, end_date)).strftime('%d.%m.%Y').tolist()
    list =[]
    for data in r:
        list.append(request(data, *args))
    return await asyncio.gather(*list)

    

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(main(10))
    for r in result:
        print(r)