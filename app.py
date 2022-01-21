import streamlit as st
import pandas as pd
import altair as alt
from scrape_scripts import racename_raceid


# サイドバー
st.sidebar.write(
    """
    # 出走馬データ
    #####
    ##### メインレース出走馬のデータをまとめました
    ##### 以下のプルダウンからレースを選択できます
    #####
    """
)

# セレクトボックスにレース名を表示し、選択されたレース名からレースIDを取り出す
racename_raceid_dict = racename_raceid.racename_raceid()
racename = st.sidebar.selectbox('レース名',list(racename_raceid_dict.keys()))
raceid = racename_raceid_dict[racename]

# 出走馬データを読み込み、馬名をリスト化して、二次元配列から一次元配列に整形する
entry_horse_df = pd.read_pickle('./pickles/entry_list.pickle')
entry_horse_list = sum(entry_horse_df.loc[raceid]['馬名'].values.tolist(), [])


# メインのカラム
st.write(
    f"""
    ### **{racename}**
    """
)

# 加工した出馬データを読み込む
# チャートの表示用にインデックスを馬名列に変換する
horse_data_summary_df = pd.read_pickle('./pickles/horse_data_summary.pickle')
horse_data_summary_df = horse_data_summary_df.reset_index().rename(columns={'index': '馬名'})

# 選択したレースの出走馬のみのデータを作成する
extracted_summary_df = horse_data_summary_df[horse_data_summary_df['馬名'].isin(entry_horse_list)]

# 表を表示
# TODO表の列名が見切れるので、調整したい
st.dataframe(extracted_summary_df)

# チャートを表示
horse_data_for_chart = (
    alt.Chart(extracted_summary_df)
    .mark_circle(opacity=0.8, clip=True)
    .interactive()
    .encode(
        x=alt.X('1000m平均タイム（s）', stack=None, scale=alt.Scale(domain=[55,65])),
        y=alt.Y('上がり3F平均タイム（s）:Q', stack=None, scale=alt.Scale(domain=[30,40])),
        color='馬名',
        tooltip=['馬名', '1000m平均タイム（s）', '上がり3F平均タイム（s）']
    )
)
st.altair_chart(horse_data_for_chart, use_container_width=True)
