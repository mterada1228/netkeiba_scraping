from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from model.raceResult import RaceResult
from model.hose import Hose
from model.hoseRaceResult import HoseRaceResult
import matplotlib
import matplotlib.pyplot as plt

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

    # Hose データの取得
    hoseRaceResults = getHoseRaceResult(session, '2010100690')

    # Session クローズ
    session.close()

    # グラフにプロットする
    dataPlot(hoseRaceResults)

def getHoseRaceResult(session, hose_id):

    hoseRaceResults = session.query(Hose, HoseRaceResult, RaceResult)\
        .filter(Hose.hose_id == hose_id)\
            .filter(Hose.hose_id == HoseRaceResult.hose_id)\
                .filter(HoseRaceResult.race_id == RaceResult.id)

    return hoseRaceResults

def dataPlot(hoseRaceResults):

    """ グラフを描画する """

    # 日本語フォントを有効にする
    matplotlib.rcParams['font.sans-serif'] = 'MigMix 1P'    

    # dataをplotする
    for hoseRaceResult in hoseRaceResults:
        plt.plot(hoseRaceResult.RaceResult.RPCI, hoseRaceResult.RaceResult.ave_1F, 'ro', label=hoseRaceResult.RaceResult.name)

    # グラフの体裁を整える
    plt.xlabel('RPCI')
    plt.ylabel('ave-1F')
    plt.title('RPCI x ave-1F マトリクス')
    plt.legend(loc='best') # 凡例をいい感じの位置に配置する
    plt.xlim(40, 70)
    plt.ylim(10, 14)
    plt.savefig('test_hoseRaceResult.png', dpi=300)

if __name__ == "__main__":
    main()