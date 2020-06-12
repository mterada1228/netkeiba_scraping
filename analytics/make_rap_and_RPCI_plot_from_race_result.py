from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from model.raceResult import RaceResult

import MySQLdb

def main():

    race_result = getRaceResultData()
    print(race_result)

    # TODO データをプロットする。

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

    race_result = session.query(RaceResult).all() 

    session.close()

    return race_result

if __name__ == "__main__":
    main()