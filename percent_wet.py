import pandas as pd

GWATER_CUTOFF = 2 # ft NAD88

wells = pd.read_csv('wells.csv')
percents = list()

for idx, row in wells.iterrows():
    this_df = pd.read_csv('data/csvs/{}.csv'.format(row['Dbkey']))
    gwater_depths = -(this_df['gwater_elev_navd88'] - row['Elev_NAVD88'])
    this_perc = sum(gwater_depths > GWATER_CUTOFF) / gwater_depths.size
    percents.append(this_perc)

all_data = pd.DataFrame({
    'dbkey': wells['Dbkey'],
    'latitude': wells['Latitude'],
    'longitude': wells['Longitude'],
    'x_coord': wells['X COORD'],
    'y_coord': wells['Y COORD'],
    'perc_above_{}ft'.format(GWATER_CUTOFF): percents
})

all_data.to_csv('output.csv')