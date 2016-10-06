import pandas as pd


df = pd.read_csv('data/2015denverbcycletripdata_public.csv',
                 dtype={'Zip': pd.np.object, 'Bike': pd.np.object})

# Remove Trips with a Special Event location (outside of the permanent 87 locations)
df = df[df['Return Kiosk'] != 'Special Events']
df = df[df['Return Kiosk'] != 'UMS']
df = df[df['Return Kiosk'] != 'DBS LARIMER WAREHOUSE']
df = df[df['Return Kiosk'] != 'Cherry Creek Arts Festival Event Kiosk']
df = df[df['Return Kiosk'] != 'Broncos Bike Valet']

df.to_csv('data/cleaned_data.csv', index=False)
