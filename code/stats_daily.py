import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

start_date = '2025-03-07'
end_date = '2025-04-07'
ppl_count = 5
smoothing = 600
smoothing_type = 1

# start_date = '2008-02-01'
# end_date = '2025-04-07'
# ppl_count = 1000
# smoothing = 10000
# smoothing_type = 1



colors = plt.cm.tab20.colors 


df = pd.read_csv('output2.csv')

df['Date'] = pd.to_datetime(df['Date'])

def filter_by_date(df, start_date, end_date):
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

df_filtered = filter_by_date(df, start_date, end_date)

nickname_totals = df_filtered.iloc[:, 1:].sum()

top_nicknames = nickname_totals.nlargest(ppl_count).index

plt.figure(figsize=(12, 6))

for i, nickname in enumerate(top_nicknames):
    nickname_data = df_filtered[['Date', nickname]].dropna() 
    
    x = (nickname_data['Date'] - nickname_data['Date'].min()) / np.timedelta64(1, 'D')
    y = nickname_data[nickname].values
    
    spl = make_interp_spline(x, y, k=smoothing_type)  
    x_new = np.linspace(x.min(), x.max(), smoothing) 
    y_new = spl(x_new)
    
    y_new = np.maximum(y_new, 0)
    
    color = colors[i % len(colors)]
    
    plt.fill_between(nickname_data['Date'].iloc[0] + pd.to_timedelta(x_new, 'D'), 0, y_new, 
                     color=color, alpha=0.2) 
    
    plt.plot(nickname_data['Date'].iloc[0] + pd.to_timedelta(x_new, 'D'), y_new, label=nickname, color=color)

plt.title(f'Активность ({start_date.date()} - {end_date.date()})')
plt.xlabel('Дата')
plt.ylabel('Количество постов в день')
plt.xticks(rotation=45)

plt.legend(ncol=1, loc='upper left', bbox_to_anchor=(1, 1))

plt.ylim(bottom=0) 

plt.tight_layout()  
plt.show()
