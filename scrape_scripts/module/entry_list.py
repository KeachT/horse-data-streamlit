import pandas as pd
import time

def scrape(racename_raceid_dict):
    raceid_list = list(racename_raceid_dict.values())
    entries = pd.DataFrame()

    for raceid in raceid_list:
        url = 'https://race.netkeiba.com/race/shutuba.html?race_id=' + raceid
        df = pd.read_html(url)[0]
        df.index = [raceid] * len(df)
        entries = entries.append(df)
        time.sleep(1)

    entries.to_pickle('../pickles/entry_list.pickle')