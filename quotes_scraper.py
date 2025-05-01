
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def acrape_quotes():
    #対象URL
    base_url = "http://quotes.toscrape.com/"
    url = "/"
    
    # データをためるリスト
    all_quotes = []
    
    while url:
        # ページの取得
        response = requests.get(base_url + url)
        # BeautifulSoupでHTML解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 最初の１ページから名言・作者を取得
        quotes = soup.select('div.quote')
        
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tag_elements = quote.select('div.tags a.tag')
            tags = [tag.text for tag in tag_elements]
    
            all_quotes.append({
                "quote": text,
                "author": author,
                "tags": ",".join(tags)
            })
    
        #「次のページ」があればそのURLを取得
        next_btn = soup.select_one("li.next a")
        url = next_btn["href"] if next_btn else None
    
        time.sleep(1) #アクセスが速すぎないように

    # DataFrameに変換
    df = pd.DataFrame(all_quotes)
    
    # CSVとして保存
    df.to_csv('quotes.csv', index=False)

    print("CSVファイル 'quotes.csv'を保存しました")

if __name__ == "__main__":
    scrape_quotes()
