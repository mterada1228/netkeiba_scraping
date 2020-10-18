from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from model.raceResult import RaceResult
from model.hose import Hose
from model.hoseRaceResult import HoseRaceResult
from model.raceHose import RaceHose
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import pdb

import MySQLdb

def main():

    # settings

    # DBへ接続する
    # 接続ホスト名: localhost
    # データベース名: netkeiba
    # ユーザー名: netkeiba_scraper
    # パスワード: password
    # 文字コード: utf8mb4
    engine = create_engine('mysql://netkeiba_scraper:password@localhost/netkeiba?charset=utf8mb4')

    # Session 作成
    Session = sessionmaker(bind=engine)
    session = Session()

    # HoseRaceResult データの取得
    hoseRaceResults = getHoseRaceResult(session, race_id='2014100595')

    # Session クローズ
    session.close()

    # グラフにプロットする
    # dataPlot(hoseRaceResults)
    dataPlot(hoseRaceResults)

def getHoseRaceResult(session, race_id):

    hoseRaceResults = session.query(RaceHose, Hose, HoseRaceResult, RaceResult)\
        .filter(RaceHose.race_id == race_id)\
            .filter(RaceHose.hose_id == Hose.hose_id)\
                .filter(Hose.hose_id == HoseRaceResult.hose_id)\
                    .filter(HoseRaceResult.race_id == RaceResult.id)

    return hoseRaceResults

def dataPlot(hoseRaceResults):

    """ グラフを描画する """

    # 日本語フォントを有効にする
    matplotlib.rcParams['font.sans-serif'] = 'MigMix 1P'   

    # グラフプロット
    
    x = []
    y = []

    nige_x = []
    nige_y = []
    not_nige_x = []
    not_nige_y = []

    names = []
    colorTbl = []
    sizeTbl = []

    for hoseRaceResult in hoseRaceResults:
        if hoseRaceResult.HoseRaceResult.passing_order.split('-')[0] == '1':
            nige_x.append(hoseRaceResult.RaceHose.hose_num)
            x.append(hoseRaceResult.RaceHose.hose_num)
            nige_y.append(hoseRaceResult.RaceResult.ave_1F)
            y.append(hoseRaceResult.RaceResult.ave_1F) 
            names.append(f'{hoseRaceResult.RaceResult.date} {hoseRaceResult.RaceResult.name} {hoseRaceResult.RaceResult.cource_condition} {hoseRaceResult.HoseRaceResult.passing_order}')
            colorTbl.append("red")
            sizeTbl.append(20)
        else:
            not_nige_x.append(hoseRaceResult.RaceHose.hose_num)
            x.append(hoseRaceResult.RaceHose.hose_num)
            not_nige_y.append(hoseRaceResult.RaceResult.ave_1F)
            y.append(hoseRaceResult.RaceResult.ave_1F) 
            names.append(f'{hoseRaceResult.RaceResult.date} {hoseRaceResult.RaceResult.name} {hoseRaceResult.RaceResult.cource_condition} {hoseRaceResult.HoseRaceResult.passing_order}')
            colorTbl.append("gray")
            sizeTbl.append(10)

    # 各馬の逃げレース数 / レース数を算出
    hose_num_list = list(set(nige_x + not_nige_x))
    for hose_num in hose_num_list:
        hose_race_count = len(list(filter(lambda z:z == hose_num, nige_x + not_nige_x)))
        nige_race_count = len(list(filter(lambda z:z == hose_num, nige_x)))
        x.append(hose_num)
        y.append(10)
        colorTbl.append("white")
        sizeTbl.append(20)
        names.append(f'逃げレース / 全レース: {nige_race_count}/{hose_race_count}')

    fig,ax = plt.subplots()
    sc = plt.scatter(x, y, c=colorTbl, s=sizeTbl)

    # プロットにホバーした時、凡例を表示させる
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))

    annot.set_visible(False)

    def update_annot(ind):

        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                            " ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor(colorTbl[ind["ind"][0]])
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    # グラフの体裁を整える
    plt.xlabel('馬番')
    plt.ylabel('ave-1F')
    plt.title('逃げ度数')
    plt.xlim(0, 19)
    plt.ylim(10, 14)
    grit_gap = np.arange(0, 20, 1)
    ax.set_xticks(grit_gap)
    ax.grid(which = "major", axis = "x", color = "blue", alpha = 0.8,
        linestyle = "--", linewidth = 1)
    plt.savefig('test_hoseRaceResult.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    main()