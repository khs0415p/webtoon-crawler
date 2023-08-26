from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import html_to_json
import datetime
import pandas as pd
import requests
import re


class Scraper:
    def __init__(self) -> None: # custom
        self.domain = "domain"
        self.dowurl_query = "dow_query"
        self.dowurl_cvt = "dow_cvt"
        self.fixed_xpath = True
        self.container_xpath = "container_xpath"
        self.creators_each_url = False
        self.creators_xpath = "creator_xpath"
    
    def do_scrap(self, save=True): # custom
        dfs = []
        for dow in range(7):
            elem_html = self.fetch(dow)
            dow_df = self.parse(elem_html)
            dow_df["DOW"] = dow
            dfs.append(dow_df)
        df = pd.concat(dfs, ignore_index=True)
        
        if self.creators_each_url:
            df["CREATOR"] = self.get_creators(df['LINK'])
        df["DATE"] = datetime.datetime.today().date()

        if save:
            df.to_csv(f'test_{self.__class__.__name__}.csv')        
        return df

    def fetch(self, dow=-1):
        driver = webdriver.Chrome()

        driver.get(self.dow_url(dow))
        self.scroll(driver, 4)
        elem = driver.find_element(By.XPATH, self.get_container_xpath(dow))
        elem_html = elem.get_attribute('innerHTML')

        driver.close()
        return elem_html
    
    def parse(self, html_str:str): # custom
        json_elem = html_to_json.convert(html_str)

        df_list = []
        for rank, toon in enumerate(self.parsing_container_path(json_elem)):
            df_list.append(self.parsing_path(rank+1, toon))
        df = pd.DataFrame(df_list)
        return df
        
    def dow_url(self, dow:int) -> str:
        return self.domain + self.dowurl_query + self.dowurl_cvt[dow]
    
    @staticmethod
    def scroll(driver, sec):
        for _ in range(0, sec*10):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
    
    def get_container_xpath(self, dow): # custom
        if self.fixed_xpath:
            return self.container_xpath
        else:
            return "요일별로 xpath가 다를 때 container_xpath"
    
    @staticmethod
    def parsing_container_path(json_elem):   # custom
        return json_elem["li"]
    
    def parsing_path(self, rank, toon): # custom
        return {
            "RANK": rank, 
            "TITLE": "parsing path title",
            "CREATOR": "parsing_path_creator",
            "LINK": self.domain + "parsing_path_link",
            "IMG_LINK": "parsing_path_imglink", 
        }
    
    def get_creators(self, links:pd.Series):
        creators = []
        driver = webdriver.Chrome()
        for url in links:
            driver.get(url)
            creator = driver.find_element(By.XPATH, self.creators_xpath).text
            creators.append(creator)
        driver.quit()
        return creators
        
class NaverScraper(Scraper):
    def __init__(self) -> None:
        super().__init__()
        self.domain = "https://comic.naver.com"
        self.dowurl_query = "/webtoon?tab="
        self.dowurl_cvt = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.container_xpath = '//*[@id="content"]/div[1]/ul'
    
    def parsing_path(self, rank, toon):
        return {
            "RANK": rank, 
            "TITLE": toon['div'][0]['a'][0]['span'][0]['span'][0]['_value'],
            "CREATOR": toon['div'][0]['a'][1]['_value'] if len(toon['div'][0]['a'])==2 else toon['div'][0]['div'][0]['a'][0]['_value'],
            "LINK": self.domain + toon['a'][0]['_attributes']['href'],
            "IMG_LINK": toon['a'][0]['div'][0]['img'][0]['_attributes']['src'], 
        }

class LezhinScraper(Scraper):
    def __init__(self) -> None:
        super().__init__()
        self.domain = "https://www.lezhin.com"
        self.dowurl_query = "/ko/scheduled?day="
        self.dowurl_cvt = ['1', '2', "3", "4", "5", "6", "0"]
        self.fixed_xpath = False
    
    def get_container_xpath(self, dow):
        return f'//*[@id="scheduled"]/div/ul[{dow+1}]'
        
    def parsing_path(self, rank, toon):
        return {
            "RANK": rank, 
            "TITLE": toon['a'][0]['div'][1]['div'][1]['_value'],
            "CREATOR": toon['a'][0]['div'][1]['div'][2]['span'][0]['_value'],
            "LINK": self.domain + toon['a'][0]['_attributes']['href'],
            "IMG_LINK": toon['a'][0]['div'][0]['picture'][0]['img'][0]['_attributes']['src'],
        }
    
class ToptoonScraper(Scraper):
    def __init__(self) -> None:
        super().__init__()
        self.domain = "https://toptoon.com"
        self.dowurl_query = "/weekly#weekly"
        self.dowurl_cvt = ['1', '2', "3", "4", "5", "6", "7"]
        self.fixed_xpath = False
        self.creators_each_url = True
        self.creators_xpath = '//*[@id="episodeBnr"]/div[2]/div[1]/div[3]/span[1]'
        
    def get_container_xpath(self, dow):
        return f'//*[@id="commonComicList"]/div/ul[{dow+1}]'
    
    def parse(self, html_str: str):
        json_elem = html_to_json.convert(html_str)

        df_list = []
        rank = 1
        for toon in self.parsing_container_path(json_elem):
            # 중간에 배너는 pass
            if "comicListBanner" in toon['_attributes']['class']:
                continue
            df_list.append(self.parsing_path(rank, toon))
            rank += 1
        df = pd.DataFrame(df_list)
        return df
    
    # @staticmethod
    # def parsing_container_path(json_elem):
    #     return json_elem["li"]
    
    def parsing_path(self, rank, toon):
        return {
            "RANK": rank, 
            "TITLE": toon['a'][0]['div'][1]['p'][0]['span'][0]['_value'],
            "LINK": self.domain + toon['a'][0]['_attributes']['href'],
            "IMG_LINK": re.findall("https?.*\.(?:jpg|png)", toon['a'][0]['div'][0]['_attributes']['style'])[0], 
        }
        
class ToomicsScraper(Scraper):
    def __init__(self) -> None:
        super().__init__()
        self.domain = "https://www.toomics.com/"
        self.dowurl_query = "/webtoon/weekly/dow/"
        self.dowurl_cvt = ["1", "2", "3", "4", "5", "6", "7"]
        self.fixed_xpath = True
        self.container_xpath = '//*[@id="more_list"]'
        self.creators_each_url = True
        self.creators_xpath = '//*[@id="contents"]/div/div[2]/main/div[1]/div[1]/dl/dd'
    
    def parsing_path(self, rank, toon):
        return {
            "RANK": rank, 
            "TITLE": toon['a'][0]['div'][1]['div'][0]['strong'][0]['_value'],
            "LINK": self.domain + '/webtoon/episode/toon/' + toon['a'][0]['_attributes']['href'].split('/')[-1],
            "IMG_LINK": toon['a'][0]['div'][0]['img'][0]['_attributes']['src'], 
        }
    

def img_overlap_from_url(sr:pd.Series, path='images'):
    """배경, 캐릭터 이미지 url을 통해 이미지를 합쳐서 저장한 뒤, 저장경로 return"""
    import requests
    from PIL import Image
    from io import BytesIO
    import os
    import re
    
    try:
        bg_response = requests.get(sr.BG_IMG_URL)
        bg_img= Image.open(BytesIO(bg_response.content))
    except:
        return None
    

    try:
        fg_response = requests.get(sr.FG_IMG_URL)
        fg_img = Image.open(BytesIO(fg_response.content))
    except:
        return None
    

    thumbnail_img = bg_img.resize(fg_img.size)
    thumbnail_img.paste(fg_img, fg_img)

    if not os.path.exists(path):
        os.makedirs(path)
    thumbnail_path = f"{path}/{re.sub('[^가-힣0-9_a-zA-Z/]', '', re.sub(' ', '_', sr.NAME))}.png"
    thumbnail_img.save(thumbnail_path)

    return thumbnail_path

def kakao_scrap():
    DOMAIN = getattr(domain_info, 'KAKAO')
    dfs = []
    
    driver = webdriver.Chrome()
    for dow in range(7):
        
        # fetch
        driver.get(DOMAIN.dow_url(dow))
        scroll(driver, 4)
        elem = driver.find_element(By.XPATH, DOMAIN.xpath)
        elem_html = elem.get_attribute('innerHTML')
        
        # parsing
        json_elem = html_to_json.convert(elem_html)
        df_list = []
        today = datetime.datetime.today().date()    # 수집날짜
        driver.get(DOMAIN.domain + json_elem['div'][0]['a'][0]['_attributes']['href'])
        creator = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[2]').text
        df_list.append( # 1위
            {
                "DATE": today, 
                'DOW': dow,
                'RANK': 1,
                'NAME': json_elem['div'][0]['a'][0]['div'][0]['div'][0]['div'][1]['picture'][0]['img'][0]['_attributes']['alt'],
                'CREATOR': creator,
                'URL': DOMAIN.domain + json_elem['div'][0]['a'][0]['_attributes']['href'],
                'BG_IMG_URL': None, 
                'FG_IMG_URL': None
            }
        ) 
        toon_rank = json_elem['div'][1]['div']  # 2위~
        for rank, toon in enumerate(toon_rank): 
            if 'a' not in toon['div'][0]['div'][0].keys():
                break
            turl = DOMAIN.domain + toon['div'][0]['div'][0]['a'][0]['_attributes']['href']
            driver.get(turl)
            creator = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[2]').text
            df_list.append(
                {
                    "DATE": today, 
                    'DOW': dow,
                    'RANK': rank + 2,
                    'NAME': toon['div'][0]['div'][0]['a'][0]['div'][2]['picture'][0]['img'][0]['_attributes']['alt'],
                    'CREATOR': creator,
                    'URL': DOMAIN.domain + toon['div'][0]['div'][0]['a'][0]['_attributes']['href'],
                    'BG_IMG_URL': toon['div'][0]['div'][0]['a'][0]['picture'][0]['img'][0]['_attributes']['src'], 
                    'FG_IMG_URL': toon['div'][0]['div'][0]['a'][0]['picture'][1]['img'][0]['_attributes']['src'], 
                }
            )
        df = pd.DataFrame(df_list)
        dfs.append(df)
    driver.close()
    
    df = pd.concat(dfs, ignore_index=True)
    df['IMG_PATH'] = df[['BG_IMG_URL', 'FG_IMG_URL', 'NAME']].apply(img_overlap_from_url, axis=1)   # 썸네일 이미지 생성 및 저장
    df.to_csv('test_kakao.csv')
    
    return elem_html
        
def Kakao_Parser(dow:str, rank_html:str) -> pd.DataFrame:
    """Kakao 웹툰의 요일별 랭킹 html에서 필요한 정보와 날짜 등을 DataFrame으로 반환해주는 함수"""
    
    # HTML -> json(dict)
    json_elem = html_to_json.convert(rank_html)

    df_list = []
    today = datetime.datetime.today().date()    # 수집날짜

    # 1위 웹툰 따로 추가
    df_list.append(
        {
            "DATE": today, 
            'DOW': dow,
            'RANK': 1,
            'NAME': json_elem['div'][0]['a'][0]['div'][0]['div'][0]['div'][1]['picture'][0]['img'][0]['_attributes']['alt'],
            'URL': KakaoWebtoon() + json_elem['div'][0]['a'][0]['_attributes']['href'],
            'BG_IMG_URL': None, 
            'FG_IMG_URL': None
        }
    ) 

    # 2위~ 웹툰들
    toon_rank = json_elem['div'][1]['div']  
    for rank, toon in enumerate(toon_rank): 
        if 'a' not in toon['div'][0]['div'][0].keys():
            break
        # parsing
        df_list.append(
            {
                "DATE": today, 
                'DOW': dow,
                'RANK': rank + 2,
                'NAME': toon['div'][0]['div'][0]['a'][0]['div'][2]['picture'][0]['img'][0]['_attributes']['alt'],
                'URL': KakaoWebtoon() + toon['div'][0]['div'][0]['a'][0]['_attributes']['href'],
                'BG_IMG_URL': toon['div'][0]['div'][0]['a'][0]['picture'][0]['img'][0]['_attributes']['src'], 
                'FG_IMG_URL': toon['div'][0]['div'][0]['a'][0]['picture'][1]['img'][0]['_attributes']['src'], 
            }
        )
    
    df = pd.DataFrame(df_list)
    
    return df
