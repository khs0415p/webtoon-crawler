import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import html_to_json
import time
import pandas as pd
import datetime

from urls import NaverWebtoon

def parse_args():
    parser = argparse.ArgumentParser()    
    args = parser.parse_args()
    
    return args

def Naver_fetcher():
    """네이버웹툰에서 요일별 랭킹 순위가 있는 영역의 html을 그대로 text로 반환해주는 함수"""
    
    driver = webdriver.Chrome()
    driver.get(NaverWebtoon()+'/webtoon')
    
    # 끝까지 스크롤
    for _ in range(0,40):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    
    # 요일별 랭킹 순위 영역
    elem = driver.find_element(By.CSS_SELECTOR, '#container > div.component_wrap.type2 > div.WeekdayMainView__daily_all_wrap--UvRFc')    
    text_elem = elem.get_attribute('innerHTML')
    
    driver.close()
    
    return text_elem

def Naver_Parser(rank_html:str) -> pd.DataFrame:
    """네이버 웹툰의 요일별 랭킹 순위가 있는 영역의 html을 입력하면 필요한 부분의 정보와 날짜 등을 DataFrame으로 반환해주는 함수"""
    
    # HTML -> json(dict)
    json_elem = html_to_json.convert(rank_html)
        
    df_list = []

    # Parsing
    today = datetime.datetime.today().date()    # 수집날짜
    
    for json_dow in json_elem['div']:
        dow = json_dow['h3'][0]['_value']   # 요일
        toon_rank = json_dow['ul'][0]['li'] # 요일별 ranking
        
        for rank, toon in enumerate(toon_rank):
        
            df_list.append(
                {
                    "DATE": today, 
                    'DOW': dow,
                    'RANK': rank+1,
                    'NAME': toon['div'][0]['a'][0]['span'][0]['span'][0]['_value'],
                    'LINK': NaverWebtoon() + toon['a'][0]['_attributes']['href'], 
                    'IMG_LINK': toon['a'][0]['div'][0]['img'][0]['_attributes']['src'],    
                }
            )
    
    df = pd.DataFrame(df_list)
    
    return df

def main():
    args = parse_args()
    
    # Naver 랭킹 가져오기: html
    rank_html = Naver_fetcher()
    
    # Naver 랭킹 Parsing: html -> dataframe
    df = Naver_Parser(rank_html)

    # 저장
    df.to_csv('test.csv')
    

if __name__=="__main__":
    main()