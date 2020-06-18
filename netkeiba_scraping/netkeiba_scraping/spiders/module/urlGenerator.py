from datetime import datetime, timedelta

def getUrls(base_url, cource_code, start_date, end_date, query=''):

    """ scrapingを実行するurlのリストを返す """

    time_diff_days = end_date - start_date + timedelta(days=1)
    time_itereter = timedelta(days=0)

    start_urls = []

    while time_diff_days > time_itereter:
        date = (start_date + time_itereter).strftime('%Y%m%d')
        round_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

        for round in round_list:
            url = base_url + date[0:4] + cource_code + date[4:8] + round + query
            start_urls.append(url)
            print(url)

        time_itereter += timedelta(days=1)

    return start_urls