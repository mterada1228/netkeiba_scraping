from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from model.raceResult import RaceResult
import matplotlib
import matplotlib.pyplot as plt

import MySQLdb

def main():
    race_results = getRaceResultData()
    dataPlot(race_results)

def getRaceResultData():
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

    race_results = session.query(RaceResult).all() 

    session.close()

    return race_results

def dataPlot(race_results):

    """ グラフを描画する """

    # 日本語フォントを有効にする
    matplotlib.rcParams['font.sans-serif'] = 'MigMix 1P'    

    # dataをplotする
    for race_result in race_results:
        plt.plot(race_result.RPCI, race_result.ave_1F, 'ro', label=race_result.name)

    # グラフの体裁を整える
    plt.xlabel('RPCI')
    plt.ylabel('ave-1F')
    plt.title('RPCI x ave-1F マトリクス')
    plt.legend(loc='best') # 凡例をいい感じの位置に配置する
    plt.xlim(40, 70)
    plt.ylim(10, 14)
    plt.savefig('test.png', dpi=300)

if __name__ == "__main__":
    main()