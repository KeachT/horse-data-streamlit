import pandas as pd

def output_summary(racename_raceid_dict):
    # レース結果、各馬のレースデータを読み込む
    race_results = pd.read_pickle('../pickles/results_sum.pickle')
    horse_results = pd.read_pickle('../pickles/horse_results.pickle')
    # 上がり列に欠損値のある行を省く
    horse_results.dropna(subset=['上り'], inplace=True)

    # 出走馬データを取り出し、馬名をリスト化する
    entry_horse_df = pd.read_pickle('../pickles/entry_list.pickle')
    raceid_list = list(racename_raceid_dict.values())
    horse_name_list = []

    for raceid in raceid_list:
        # 馬名列を取り出し、二次元配列から一次元配列に整形する
        horse_name_list.append(sum(entry_horse_df.loc[raceid]['馬名'].values.tolist(), []))

    # 馬名リストを二次元配列から一次元配列に整形する
    horse_name_list = (sum(horse_name_list, []))

    # 馬ごとに行う処理
    # 馬名リストを馬idリストに変換
    horse_id_list = []
    name_id_dict = dict(zip(race_results['馬名'], race_results['horse_id']))
    id_name_dict = dict(zip(race_results['horse_id'], race_results['馬名']))

    for i in horse_name_list:
        try:
            horse_id_list.append(name_id_dict[i])
        # horse_idが存在しない場合は処理を飛ばす
        except KeyError:
            continue

    # 加工後のデータを保存するdataframeを作成
    horse_data_summary_df = pd.DataFrame(
            columns = ['1000m平均タイム（s）', '上がり3F平均タイム（s）', '複勝率（%）']
        )


    # 馬idリストを使用して、処理をforで回す
    for horse_id in horse_id_list:

        # 馬idとカラム名を指定して、対象馬の直近５レースの結果を抽出する
        target_horse = horse_results.loc[horse_id, ['上り', '距離', 'タイム', '着順']].head(5)

        # 距離列からコース種類（芝orダ）取り除いてからInt型に変換する、タイム列をInt型の秒単位に直す、着順列をInt型に直す
        races_count = len(target_horse['距離'])
        race_distances = []
        race_times = []
        i = 0
        while i < races_count:
            race_distances.append(int(target_horse['距離'][i][1:]))

            race_time_min = float(target_horse['タイム'][i][0]) * 60
            race_time_sec = float(target_horse['タイム'][i][2:])
            race_times.append(race_time_min + race_time_sec)

            i += 1

        # 着順列をInt型に変換
        target_horse['着順'] = target_horse['着順'].astype('int')

        # データを加工した辞書型の距離とタイムを、dataframeオブジェクトに列を追加して格納する
        target_horse['race_distances'] = race_distances
        target_horse['race_times'] = race_times

        # 1000mの平均タイム
        average_race_distances = target_horse['race_distances'].mean()
        average_race_times = target_horse['race_times'].mean()
        average_race_speed = average_race_distances / average_race_times
        average_race_times_for_1000m = round(1000 / average_race_speed, 2)

        # 上がり3fの平均値
        average_race_time_for_final600m = target_horse['上り'].mean()

        # 複勝率
        races_count = len(target_horse['距離'])
        show_count = 0
        i = 0

        while i < races_count:
            if target_horse['着順'][i] <= 3:
                show_count += 1
            i += 1
        show_rate = show_count / races_count * 100

        # 結果をdataframeに格納する
        extracted_horse_data_df = pd.DataFrame(
            data = [{'1000m平均タイム（s）': average_race_times_for_1000m, '上がり3F平均タイム（s）': average_race_time_for_final600m, '複勝率（%）': show_rate}],
            index = [id_name_dict[horse_id]]
        )
        horse_data_summary_df = horse_data_summary_df.append(extracted_horse_data_df)

    # 加工したデータをpickleに保存
    horse_data_summary_df.to_pickle('../pickles/horse_data_summary.pickle')