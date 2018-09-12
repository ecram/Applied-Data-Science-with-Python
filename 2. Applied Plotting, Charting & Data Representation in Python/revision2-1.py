
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df[(df['Date'] >= '2005.01.01') & (df['Date'] <= '2015.12.31')]
df = df.sort(columns=['Date'], ascending=True, inplace=False)
df['monthsdays'] = df['Date'].apply(lambda x: x.strftime('%m.%d'))
df['Data_Value'] = df['Data_Value']
df = df[df['monthsdays'] != '02.29']
df

%matplotlib notebook

def get_df_for_date_interval(df):
    return df[(df['Date'] >= '2005.01.01') & (df['Date'] <= '2014.12.31')]

def get_tmaxes(df):
    tmaxes = get_df_for_date_interval(df)
    tmaxes = tmaxes[tmaxes['Element'] == 'TMAX']
    tmaxes = tmaxes.groupby(by=['monthsdays'], as_index=False)['Data_Value'].max()
    tmaxes['monthsdays'] = pd.to_datetime(tmaxes['monthsdays'], format='%m.%d')
    return tmaxes

def get_tmins(df):
    tmins = get_df_for_date_interval(df)
    tmins = tmins[tmins['Element'] == 'TMIN']
    tmins = tmins.groupby(by=['monthsdays'], as_index=False)['Data_Value'].min()
    tmins['monthsdays'] = pd.to_datetime(tmins['monthsdays'], format='%m.%d')
    return tmins

def get_daily_max_record(df):
    return df.loc[df['Data_Value'].idxmax()]

def get_daily_min_record(df):
    return df.loc[df['Data_Value'].idxmin()]

def get_max_records(df, tmaxes):
    df2 = tmaxes.copy()
#     df2 = df2.groupby('monthsdays').apply(get_daily_max_record)

    df2015 = df[(df['Date'] >= '2015.01.01') & (df['Date'] <= '2015.12.31') & (df['Element'] == 'TMAX')]
    df2015 = df2015.groupby('Date').max()
    
    df2015['monthsdays'] = pd.to_datetime(df2015['monthsdays'], format='%m.%d')

    df2 = df2.merge(df2015, left_on='monthsdays', right_on='monthsdays', how='inner')
    return df2[df2['Data_Value_x'] < df2['Data_Value_y']]
    
def get_min_records(df, tmaxes):
    df2 = tmaxes.copy()
#     df2 = df2.groupby('monthsdays').apply(get_daily_min_record)

    df2015 = df[(df['Date'] >= '2015.01.01') & (df['Date'] <= '2015.12.31') & (df['Element'] == 'TMIN')]
    df2015 = df2015.groupby('Date').min()
    
    df2015['monthsdays'] = pd.to_datetime(df2015['monthsdays'], format='%m.%d')

    df2 = df2.merge(df2015, left_on='monthsdays', right_on='monthsdays', how='inner')
    return df2[df2['Data_Value_x'] > df2['Data_Value_y']]

tmaxes = get_tmaxes(df)
tmins = get_tmins(df)

plt.figure()
plt.plot(tmaxes['monthsdays'], tmaxes['Data_Value'], '-', color='red', alpha=0.3, label='Daily max temprature (tenths of degrees C)')
plt.plot(tmins['monthsdays'], tmins['Data_Value'], '-', color='blue', alpha=0.3, label='Daily min temprature (tenths of degrees C)')

plt.gca().fill_between(tmins.set_index('monthsdays').index, 
                       tmins['Data_Value'], tmaxes['Data_Value'], 
                       facecolor='black', 
                       alpha=0.1)

max_records = get_max_records(df, tmaxes)
min_records = get_min_records(df, tmins)

plt.plot_date(x=max_records['monthsdays'], y=max_records['Data_Value_y'], marker='o', color='red', linewidth=1, label='Broken high temperature record in 2015')
plt.plot_date(x=min_records['monthsdays'], y=min_records['Data_Value_y'], marker='o', color='blue', linewidth=1, label='Broken low temperature record in 2015')

plt.ylabel('Temperature in tenths of degrees C')
plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1))
plt.title('Daily highest and lowest temperature and \ndaily records broken in 2015 (tenths of degrees C)')

ax = plt.gca()
ax.grid(True, axis='y', which='both')

for spine in ax.spines.values():
    spine.set_visible(False)
    
ax.tick_params(axis=u'both', which=u'both',length=0)

from matplotlib.dates import DateFormatter

ax.xaxis.set_major_formatter(DateFormatter('%b'))

plt.savefig(
    "temp_records.png",
    bbox_inches="tight",
    papertype='a1')






