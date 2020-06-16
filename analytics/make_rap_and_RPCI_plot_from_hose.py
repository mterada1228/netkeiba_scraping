from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from model.raceResult import RaceResult
from model.hose import Hose
from model.hoseRaceResult import HoseRaceResult
import matplotlib
import matplotlib.pyplot as plt

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
    hoseRaceResults = getHoseRaceResult(session, '2014104249')

    # RaceResult　データの取得
    raceResults = getRaceResult(session, "函館スプリント")

    # Session クローズ
    session.close()

    # グラフにプロットする
    # dataPlot(hoseRaceResults)
    dataPlot(hoseRaceResults, raceResults)

def getHoseRaceResult(session, hose_id):

    hoseRaceResults = session.query(Hose, HoseRaceResult, RaceResult)\
        .filter(Hose.hose_id == hose_id)\
            .filter(Hose.hose_id == HoseRaceResult.hose_id)\
                .filter(HoseRaceResult.race_id == RaceResult.id)

    return hoseRaceResults

def getRaceResult(session, raceName):

    raceResults = session.query(RaceResult).filter(RaceResult.name.like(f'%{raceName}%'))

    return raceResults

def dataPlot(hoseRaceResults, raceResults=None):

    """ グラフを描画する """

    # 日本語フォントを有効にする
    matplotlib.rcParams['font.sans-serif'] = 'MigMix 1P'   

    # グラフプロット
    x = [ hoseRaceResult.RaceResult.RPCI for hoseRaceResult in hoseRaceResults ]
    y = [ hoseRaceResult.RaceResult.ave_1F for hoseRaceResult in hoseRaceResults ]
    names = [ f'{hoseRaceResult.RaceResult.date} {hoseRaceResult.RaceResult.name} ' for hoseRaceResult in hoseRaceResults ]

    """ 
        着差ごとにplotは色分けする 
        　・1着 -> 黄色
        　・~0.4s 差 -> 緑
        　・0.4s~1.0s 差 -> 青
        　・1.0s〜 差 -> 灰色    
    """

    colorTbl = []
    for index, hoseRaceResult in enumerate(hoseRaceResults):
        try:
            if hoseRaceResult.HoseRaceResult.rank == '1':
                colorTbl.append('yellow')
            elif float(hoseRaceResult.HoseRaceResult.time_diff) <= 0.4:
                colorTbl.append('green')
            elif float(hoseRaceResult.HoseRaceResult.time_diff) <= 1.0:
                colorTbl.append('blue')
            else:
                colorTbl.append('gray')
        except ValueError as e:
            print(f'race_id: {hoseRaceResult.HoseRaceResult.race_id} 競争除外レースのため結果から外します。')
            # グラフから競争除外のレースのプロットを除外
            del x[index]
            del y[index]
            del names[index]
            continue            

    # RaceResultsを受け取った場合はプロットする
    if raceResults != None:
        for raceResult in raceResults:
            x.append(raceResult.RPCI)
            y.append(raceResult.ave_1F)
            names.append(f'{raceResult.date} {raceResult.name}')
            colorTbl.append("red")

    fig,ax = plt.subplots()
    sc = plt.scatter(x, y, c=colorTbl)

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
    plt.xlabel('RPCI')
    plt.ylabel('ave-1F')
    plt.title(f'{hoseRaceResults[0].Hose.name} \n RPCI x ave-1F マトリクス')
    plt.xlim(40, 70)
    plt.ylim(10, 14)
    plt.savefig('test_hoseRaceResult.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    main()