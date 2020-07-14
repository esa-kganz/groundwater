import pandas as pd

URL_BASE = 'https://my.sfwmd.gov/dbhydroplsql/web_io.report_process?'

def create_request_url(**kwargs):
    defaults = {
        'v_target_code': 'file_csv',
        'v_run_mode': 'onLine',
        'v_js_flag': 'Y',
        'v_report_type': 'format6',
        'v_period': 'uspec',
        'v_dbkey': None
    }
    defaults.update(kwargs)
    url_args = ['{}={}'.format(key, defaults[key]) for key in defaults]

    global URL_BASE
    return URL_BASE + '&'.join(url_args)

if __name__ == '__main__':
    wells = pd.read_csv('wells.csv')
    percents = []

    for idx, row in wells.iterrows():
        dbkey = row['Dbkey'].strip()
        navd_correction = float(row['NAVD 88 Correction'])
        print("Dbkey: {}\tCorrection: {}".format(dbkey, navd_correction))
        request_url = create_request_url(v_dbkey=dbkey)
        try:
            this_df = pd.read_csv(request_url, skiprows=3) # skip the header info
            # Drop NAs, convert from NGVD29 to NAVD88
            this_df['Data Value'] = this_df['Data Value'].dropna().astype(float) + navd_correction
            this_df.rename(columns={'Data Value':'gwater_elev_navd88'}, inplace=True)
            this_df.to_csv('data/csvs/{}.csv'.format(dbkey))
        except Exception as e:
            print("Failed on {}: {}".format(dbkey, str(e)))
            perc_wet = None
