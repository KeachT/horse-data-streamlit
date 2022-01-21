import pandas as pd
import results
import horse_results

def main():
    # 回数を指定して、1月分までをスクレイピングする
    kai = 1
    race_id_list = []
    for place in range(1, 11, 1):
        # for kai in range(1, 13, 1):
            for day in range(1, 13, 1):
                for r in range(1, 13, 1):
                    race_id = "2022" + str(place).zfill(2) + str(kai).zfill(2) + str(day).zfill(2) + str(r).zfill(2)
                    race_id_list.append(race_id)
    results_2022 = results.scrape(race_id_list)
    results_2022.to_pickle('../pickles/2022_results.pickle')

    # 去年と今年のresultをまとめ、pickleに保存する
    results_2021 = pd.read_pickle('../pickles/2021_results.pickle')
    results_sum = pd.concat([results_2021, results_2022])
    results_sum.to_pickle('../pickles/results_sum.pickle')

    # horse_resultsをスクレイピングし、アップデートする
    results_sum = pd.read_pickle('../pickles/results_sum.pickle')
    results_sum.dropna(subset=['horse_id'], inplace=True)
    horse_id_list = results_sum['horse_id'].unique()
    horse_results_df = horse_results.scrape(horse_id_list)
    horse_results_df.to_pickle('../pickles/horse_results.pickle')

if __name__ == '__main__':
    main()