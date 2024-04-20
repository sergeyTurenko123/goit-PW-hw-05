from datetime import datetime, timedelta
import pandas as pd

start_date = datetime.now()
end_date = start_date - timedelta(days=10)

res = pd.date_range(
    min(start_date, end_date),
    max(start_date, end_date)
).strftime('%d.%m.%Y').tolist()
print(res)