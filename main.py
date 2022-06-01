from time import sleep

import pandas as pd
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import model.restaurant
import model.review_crawling
import service.restaurant_service
import service.review_crawling_service
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')
chromedriver_path = "chromedrive 3"
# driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)
# driver = webdriver.Chrome(executable_path='/Users/andes/PycharmProjects/pythonProject/chromedriver2')
driver = webdriver.Chrome(ChromeDriverManager().install())

restaurant_service = service.restaurant_service.Restaurant_service()
review_crawling_service = service.review_crawling_service.Review_crawling_service()

keyword1 = ['비건', '콩고기', '채식하는', '베지테리언', '베지', '테리언']
keyword2 = ['키즈존', '노키즈존', '유아석', '유아의자', '아기랑', '아이랑', '어린이', '유아', '아이와', '아기와', '애기와', '큰애', '작은애', '아이메뉴',
            '아기메뉴', '키즈메뉴']
keyword3 = ['독립공간', '개별공간', '상견례', '프라이빗', '독립룸', '개별룸', '예약룸']
keyword4 = ['반려견', '강아지', '애완동물', '소형견', '대형견', '반려동물']


def read(file):
    df = pd.read_csv(file, encoding="cp949")
    return df


def main():
    global driver, load_wb, review_num

    driver.implicitly_wait(4)  # 렌더링 될 때까지 4초 대기
    driver.get('https://map.kakao.com/')
    df = read('./data/1001건(1)예진_완료.csv')
    pd.set_option('display.max_columns', None)
    df = df.loc[df['영업상태코드'] == 1]
    global store
    store = df['사업장명']
    store = store.values
    store_list = store.tolist()
    global address
    address = df['도로명주소_검색용']
    address = address.values
    address = address.tolist()

    for i in range(len(store_list)):
        print('for문 인덱스버전 확인 ' + store_list[i] + address[i])
        search(store_list[i], address[i])
        continue
    driver.quit()
    print("finish")
    # print("세은 git clone test~~~~~~~~!!!!!")


def search(place_csv, addr_csv):
    global driver
    restaurant = model.restaurant.Restaurant(
        original_name="",
        name="",
        address="",
        local="",
        operation="",
        number="",
        infodttm="",
        star=0.0
    )
    search_area = driver.find_element(By.XPATH, "//*[@id=\"search.keyword.query\"]")
    search_area.send_keys('마포 ' + place_csv)  # 검색어 입력
    restaurant.original_name = place_csv
    driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    sleep(2)
    # 1번 페이지 place list 읽기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        place_lists = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name ')[0].text
        place_address = soup.select('.info_item > .addr > p')[0].text
        restaurant.address = place_address
        if (place_lists in place_csv) & (addr_csv in place_address):
            print('place가 더 긴 경우')
            crawling(place_lists, restaurant)
        elif (place_csv in place_lists) & (addr_csv in place_address):
            print('place_lists가 더 긴 경우')
            crawling(place_lists, restaurant)
        else:
            print('불일치')
    except (NoSuchElementException, ElementNotInteractableException, IndexError) as e:
        print("---검색 결과 없음!---")
        print(e)
    except StaleElementReferenceException:
        # TODO PC 환경에 따른 Stale exception 처리해야 함
        print("Stale element error 남 ~~~~~~~~~")
        print(place_lists)
        print(restaurant)
        sleep(10)
        crawling(place_lists, restaurant)

    sleep(2)
    search_area.clear()


def crawling(place_lists, restaurant):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    while_flag = False  # 수정(false->False)
    try:
        place_name = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name ')[0].text
        restaurant.name = place_name
        place_star = soup.select('.placelist > .PlaceItem > .rating > .score > .num ')[0].text
        restaurant.star = place_star
        # place_address = soup.select('.info_item > .addr > p')[0].text  # place address(도로명주소.지번은 class='lot_number')
        detail_page_xpath = driver.find_element(By.XPATH,
                                                '//*[@id="info.search.place.list"]/li[1]/div[5]/div[4]/a[1]')  # 세은해결
        detail_page_xpath.send_keys(Keys.ENTER)
        driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환 / 탭을 객체 리스트로 반환. 즉 맨 마지막 탭으로 이동하는 함수
        sleep(2)
        print('####', place_name, ' ', place_star)
    except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, IndexError) as e:
        print('&&&&&&&&&&&&&&&&&&&')
        print(e)
        '''
    try:
        for i, place in enumerate(place_lists):
            #문제ㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔㅔ
            place_name = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name ')[0].text
            restaurant.name = place_name
            place_star = soup.select('.placelist > .PlaceItem > .rating > .score > .num ')[0].text
            restaurant.star = place_star
            # place_address = soup.select('.info_item > .addr > p')[0].text  # place address(도로명주소.지번은 class='lot_number')
            print(i)
            detail_page_xpath = driver.find_element(By.XPATH, '//*[@id="info.search.place.list"]/li[' + str(
                i + 1) + ']/div[5]/div[4]/a[1]')  # 세은해결
            detail_page_xpath.send_keys(Keys.ENTER)
            driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환 / 탭을 객체 리스트로 반환. 즉 맨 마지막 탭으로 이동하는 함수
            sleep(2)
            print('####', place_name, ' ', place_star)
    except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, IndexError) as e:
        print('&&&&&&&&&&&&&&&&&&&')
        print(e)
    '''
    idx = 1
    extract_review(restaurant)  # 리뷰 추출
    # time.sleep(3)

    idx = 2
    while True:
        try:
            driver.find_element(By.XPATH, "//a[@data-page='" + str(idx) + "']").send_keys(Keys.ENTER)
            sleep(3)
            extract_review(restaurant)
            if (idx % 5 == 0):
                driver.find_element(By.LINK_TEXT, '다음').send_keys(Keys.ENTER)  # 5페이지가 넘는 경우 다음 버튼 누르기
                idx += 1
            else:
                idx += 1
                sleep(1)
        except (
                NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException,
                IndexError) as e:
            # print(idx)
            print("no review in crawling")
            print(e)
            # TODO list index out of range 걸려서 나머지 리뷰 크롤링 안 하고 다음 식당으로 넘어감
            break

    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환
    # Todo break why?
    # break


def extract_review(restaurant):
    global driver
    ret = True
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        place_update = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/span/span[1]').text
        restaurant.infodttm = place_update
        print('update: ', place_update)
    except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, IndexError) as e:
        print("no place_update information")
        print(e)

    try:
        place_call = driver.find_element(By.CLASS_NAME, 'txt_contact').text
        restaurant.number = place_call
        print('대표번호: ', place_call)

    except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, IndexError) as e:
        print("no place_call information")
        print(e)

    try:
        detail_operation = driver.find_element(By.CLASS_NAME, 'btn_more')
        detail_operation.send_keys(Keys.ENTER)
        elem = driver.find_element(By.CLASS_NAME, 'location_detail.openhour_wrap.open_on').text
        operation_time = driver.find_element(By.CLASS_NAME, 'inner_floor').text
        restaurant.operation = operation_time.replace("\n", " ").replace("닫기", "")
    except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, IndexError) as e:
        print(e)
        try:
            operation_time = driver.find_element(By.CLASS_NAME, 'location_detail.openhour_wrap').text
            restaurant.operation = operation_time.replace("\n", " ").replace("닫기", "")
            print(operation_time)
        except(
                NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException,
                IndexError) as e:
            print("no detailed operation_time information")
            print(e)

    # save restaurant

    try:
        id = restaurant_service.get_id(restaurant)
        if not id:
            id = restaurant_service.save(restaurant)
        restaurant.id = id
    except Exception as e:
        print(e, '1')
        return ret
    # TODO id=0으로 불러오는 가게들 별도로 기록
    if id == 0:
        print("fail restaurant : ", restaurant)
        return ret

    # 첫 페이지 리뷰 목록 찾기
    review_lists = soup.select('.list_evaluation > li')  # class명 없어서 그냥 li 쓴건가?
    # 리뷰가 있는 경우
    # result_review = []
    if len(review_lists) != 0:
        for i, review in enumerate(review_lists):
            comment = review.select('.comment_info > .txt_comment > span')  # 리뷰
            # rating = review.select('.grade_star size_s > em')  # 별점
            writername = review.select('.comment_info > .append_item > .link_user ')[0].text  # 작성자
            writedt = review.select('.comment_info > .append_item > .time_write ')[0].text  # 작성일자
            print('@@@@@@@@@@@@@@', writername, writedt)
            if len(comment) != 0 and len(comment[0].text) > 0:
                review_crawling = model.review_crawling.Review_crawling(
                    content=comment[0].text,
                    writer=writername,
                    writedttm=writedt,
                    restaurant=restaurant
                )
                print("review_crawling : ", review_crawling)
                try:
                    review_crawling_service.save(review_crawling=review_crawling)
                except Exception as e:
                    print(e, '2')
                    continue
            # TODO 키워드 포함이면 category_review 테이블에 txt 삽입
            # TODO 일일이 반복문 돌아서 검사하면 너무 무거우려나?

        # keyword
        try:
            for keyword in keyword1:
                if keyword in review_crawling.content:
                    start = review_crawling.content.find(keyword)
                    end = start + len(keyword)
                    txt = review_crawling.content[max(0, start - 10):min(len(review_crawling.content), end + 10)]
                    category_review = model.category_review.Category_Review(
                        category_id=1,
                        restaurant_id=review_crawling.restaurant.id,
                        txt=txt
                    )
                    insert_category_review(category_review)
        except Exception as e:
            print('keyword1 error ', e)
            
        try:
            for keyword in keyword2:
                if keyword in review_crawling.content:
                    start = review_crawling.content.find(keyword)
                    end = start + len(keyword)
                    txt = review_crawling.content[max(0, start - 10):min(len(review_crawling.content), end + 10)]
                    category_review = model.category_review.Category_Review(
                        category_id=2,
                        restaurant_id=review_crawling.restaurant.id,
                        txt=txt
                    )
                    insert_category_review(category_review)
        except Exception as e:
            print('keyword2 error ', e)

        try:
            for keyword in keyword3:
                if keyword in review_crawling.content:
                    start = review_crawling.content.find(keyword)
                    end = start + len(keyword)
                    txt = review_crawling.content[max(0, start - 10):min(len(review_crawling.content), end + 10)]
                    category_review = model.category_review.Category_Review(
                        category_id=3,
                        restaurant_id=review_crawling.restaurant.id,
                        txt=txt
                    )
                    insert_category_review(category_review)
        except Exception as e:
            print('keyword3 error ', e)

        try:
            for keyword in keyword4:
                if keyword in review_crawling.content:
                    start = review_crawling.content.find(keyword)
                    end = start + len(keyword)
                    txt = review_crawling.content[max(0, start - 10):min(len(review_crawling.content), end + 10)]
                    category_review = model.category_review.Category_Review(
                        category_id=4,
                        restaurant_id=review_crawling.restaurant.id,
                        txt=txt
                    )
                    insert_category_review(category_review)
        except Exception as e:
            print('keyword4 error ', e)



    else:
        print('no review in extract')
        ret = False
    return ret


def insert_reastaurant_locat_data_to_DB():
    result = read_reastaurant_from_db()
    for data in result:
        restaurant = model.restaurant.Restaurant(
            original_name=data[1],
            name=data[2],
            address=data[3],
            local=data[4],
            operation=data[5],
            number=data[6],
            infodttm=str(data[8]),
            star=float(data[9]),
        )

        insert_reastaurant(restaurant, regdttm=str(data[7]))


def read_reastaurant_from_db():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1q2w3e4r!',
                           db='test_db',
                           charset='utf8')

    sql = "SELECT * FROM restaurant"

    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


def insert_reastaurant(restaurant, regdttm):
    conn = pymysql.connect(host='alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com',
                           user='root',
                           password='1q2w3e4r!',
                           db='alpha',
                           charset='utf8')
    print(
        restaurant.original_name + ", " + restaurant.name + ", " + restaurant.address + ", " + restaurant.local + ", " + restaurant.operation + ", " + restaurant.number + ", " + regdttm + ", " + restaurant.infodttm + ", " + str(
            restaurant.star))

    sql = "INSERT INTO restaurant (original_name, name, address, local, operation, number, regdttm, infodttm, star) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                restaurant.original_name, restaurant.name, restaurant.address, restaurant.local, restaurant.operation,
                restaurant.number, regdttm, restaurant.infodttm, restaurant.star))
            conn.commit()


def read_review_from_db():
    conn = pymysql.connect(host='alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com',
                           user='root',
                           password='1q2w3e4r!',
                           db='alpha',
                           charset='utf8')

    sql = "SELECT * FROM review_crawling"

    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


def insert_review_locat_data_to_DB():
    reviews = read_review_from_db()
    for review in reviews:
        review_crawling = model.review_crawling.Review_crawling(
            content=review[2],
            writer=review[4],
            writedttm=review[5],
            restaurant=int(review[1])
        )

        insert_review(review_crawling)

        for keyword in keyword1:
            if keyword in review_crawling.content:
                start = review_crawling.content.find(keyword)
                end = start + len(keyword)
                txt = review_crawling.content[max(0, start - 10):min(len(review_crawling.content), end + 10)]
                category_review = model.category_review.Category_Review(
                    category_id=1,
                    restaurant_id=review_crawling.restaurant,
                    txt=txt
                )
                insert_category_review(category_review)

        for keyword in keyword2:
            if keyword in review_crawling.content:
                start = review_crawling.content.find(keyword)
                end = start + len(keyword)
                txt = review_crawling.content[max(0, start - 10):min(len(review_crawling.content), end + 10)]
                category_review = model.category_review.Category_Review(
                    category_id=2,
                    restaurant_id=review_crawling.restaurant,
                    txt=txt
                )
                insert_category_review(category_review)

        for keyword in keyword3:
            if keyword in review_crawling.content:
                start = review_crawling.content.find(keyword)
                end = start + len(keyword)
                txt = review_crawling.content[max(0, start - 10):min(len(review_crawling.content), end + 10)]
                category_review = model.category_review.Category_Review(
                    category_id=3,
                    restaurant_id=review_crawling.restaurant,
                    txt=txt
                )
                insert_category_review(category_review)

        for keyword in keyword4:
            if keyword in review_crawling.content:
                start = review_crawling.content.find(keyword)
                end = start + len(keyword)
                txt = review_crawling.content[max(0, start - 10):min(len(review_crawling.content), end + 10)]
                category_review = model.category_review.Category_Review(
                    category_id=4,
                    restaurant_id=review_crawling.restaurant,
                    txt=txt
                )
                insert_category_review(category_review)


def insert_review(review_crawling):
    conn = pymysql.connect(host='alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com',
                           user='root',
                           password='1q2w3e4r!',
                           db='alpha',
                           charset='utf8')

    sql = "INSERT INTO review_crawling (restaurant_id, content, report, writer, writedttm) " \
          "VALUES (%s, %s, %s, %s, %s)"
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                review_crawling.restaurant, review_crawling.content, review_crawling.report, review_crawling.writer,
                review_crawling.writedttm))
            conn.commit()


def insert_category_review(category_review):
    conn = pymysql.connect(host='alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com',
                           user='root',
                           password='1q2w3e4r!',
                           db='alpha',
                           charset='utf8')

    sql = "INSERT INTO category_review (category_id, txt, restaurant_id) " \
          "VALUES (%s, %s, %s)"
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                category_review.category_id, category_review.txt, category_review.restaurant_id))
            conn.commit()


if __name__ == "__main__":
    main()
