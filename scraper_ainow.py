from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import time
import csv
import datetime

# 取得する日数を決定
class ScrapingAinow():

    def execute(self, scraping_date=10):    
        scraping_dates = []
        today = str(datetime.date.today())[-2:]
        for num in range(scraping_date):
            scraping_dates.append(str(int(today)-num))

        url = "https://ainow.ai/"

        # URLにアクセスする htmlが帰ってくる
        html = urllib.request.urlopen(url=url)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")
        all_article = soup.find_all("a")

        article_titles = []
        article_urls = []
        aritcle_dates = []
        flag=1

        for tag in all_article:
            print("----------------------------------------")
            print(str(flag)+"記事目")
            flag += 1
            try:
                # "rel"が"bookmarkの場合に処理
                print(str(tag.get("rel")))
                if str(tag.get("rel").pop(0)) in "bookmark":
                    # 記事の情報を取得
                    article_url = str(tag.get("href"))
                    article_title = str(tag.get("title"))
                    article_date = article_url[-10:][:2]
                    print(article_date)
                    # 今日の記事のみ取得
                    if article_date in scraping_dates :
                        print(str(tag))            
                        print(article_url)
                        article_urls.append(article_url)
                        print(article_title)
                        article_titles.append(article_title)
            except:
                # パス→何も処理を行わない
                pass

        print(article_urls)
        print(article_titles)
        return article_urls, article_titles

if __name__ == "__main__":
    scraping = ScrapingAinow()
    article_urls, article_titles = scraping.execute()
    print(article_urls)
    print(article_titles)