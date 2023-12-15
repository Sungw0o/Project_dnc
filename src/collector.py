from datetime import datetime, timedelta
import math
import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

from src.service_news import get_news


def news_collector(category, page=1, count=1):
    collect_list = [] # 향후 데이터프레임 변환용!
    while True:
        # 수업에만 사용
        if page == 3:
            break

        url = f"https://news.daum.net/breakingnews/{category}?page={page}"
        result = requests.get(url)

        if result.status_code == 200:
            print("URL 접속 성공 → 데이터를 수집합니다.")
            doc = BeautifulSoup(result.text, "html.parser")
            url_list = doc.select("ul.list_news2 a.link_txt")

            if len(url_list) == 0:
                break

            for url in url_list:
                count += 1
                print(f"{count}", "=" * 150)
                data = get_news(url["href"], category)
                print("zzzzzzzzzzzzzzzz", data["date"])
                collect_list.append(data)

        else:
            print("잘못된 URL 경로입니다. 다시 한 번 확인해주세요.")
        page += 1

    col_name = ["category", "title", "content", "date"]
    df_reviews = pd.DataFrame(collect_list, columns=col_name)

    return df_reviews, count