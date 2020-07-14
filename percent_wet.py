import pandas as pd

def sanitize_latlon(x):
    '''
    Converts concatenated coordinates of the form
    DDMMSS.ssss... to decimal degrees.
    '''
    deg = x // 10000
    x -= deg * 10000

    min = x // 100
    x -= min * 100

    sec = x

    return deg + (min / 60) + (sec / 3600)

GWATER_CUTOFF = 2 # ft NAD88

if __name__ == '__main__':
    wells = pd.read_csv('wells.csv')
    percents = list()

    for idx, row in wells.iterrows():
        this_df = pd.read_csv('data/csvs/{}.csv'.format(row['Dbkey']))
        gwater_depths = -(this_df['gwater_elev_navd88'] - row['Elev_NAVD88'])
        this_perc = sum(gwater_depths > GWATER_CUTOFF) / gwater_depths.size
        percents.append(this_perc)

    all_data = pd.DataFrame({
        'dbkey': wells['Dbkey'],
        'latitude': wells['Latitude'].map(sanitize_latlon),
        'longitude': wells['Longitude'].map(sanitize_latlon) * -1, # E to W
        'x_coord': wells['X COORD'],
        'y_coord': wells['Y COORD'],
        'perc_above_{}ft'.format(GWATER_CUTOFF): percents
    })

    all_data.to_csv('output.csv')