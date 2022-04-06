import openpyxl
import pandas as pd
import numpy as np
from pandas import ExcelWriter

def read(file):
    df = pd.read_csv(file, encoding="cp949")
    return df

def test():
    df = read('./data/shops.csv')
    pd.set_option('display.max_columns', None)
    # print(df.columns)
    df = df.loc[df['영업상태코드'] == 1]
    # df = df[['영업상태코드', '사업장명', '전화번호', '지번주소', '도로명주소', '좌표정보(X)', '좌표정보(Y)', '데이터갱신일자', '위생업태명']]

    store = df['사업장명']
    store = store.values
    store = store.tolist()
    print(store)
    print(type(store[0]))
if __name__ == '__main__': #(한 시트에 중복으로 저장됨)
    global excel
    excel = openpyxl.Workbook()
    global sheet1
    sheet1 = excel.active
    global sheet2
    sheet2 = excel.active
    # 시트 제목 및 컬럼 이름 정의
    sheet1.title = "상호 크롤링"
    sheet1.append(['상호명_카카오', '상호명_공공', '주소_카카오', '주소_공공', '전화번호_카카오', '업데이트날짜_카카오'])
    sheet1.append(['엉클파닭', '1234', '7ㅗㅇ', '463', '111', '888'])
    sheet2.title = "상호별 리뷰 크롤링"
    sheet2.append(['상호명_카카오', '리뷰', '별점', '작성날짜'])
    sheet1.append(['교촌치킨', '379', '22957', '5922', '03', '56222'])
    excel.save('store_result.xlsx')



'''
def save() :
    # 엑셀 생성 및 활성화
    global excel
    excel = openpyxl.Workbook()
    global sheet1
    sheet1 = excel.active
    global sheet2
    sheet2 = excel.active
    # 시트 제목 및 컬럼 이름 정의
    sheet1.title = "상호 크롤링"
    sheet1.append(['상호명_카카오', '상호명_공공', '주소_카카오', '주소_공공', '전화번호_카카오', '업데이트날짜_카카오'])
    sheet1.append(['엉클파닭', '1234', '7ㅗㅇ', '463', '111', '888'])
    excel.save('store_result.xlsx')

    #sheet2.title = "상호별 리뷰 크롤링"
    #sheet2.append(['상호명_카카오', '리뷰', '별점', '작성날짜'])
    # 가게 정보 엑셀에 저장하기
    tit_rows = soup.select(' .basicInfo > .basicInfoTop > .place_details > inner_place > .tit_location ')[0].text  # 상호명
    print(tit_rows)
    addr_rows = soup.selct('.placeinfo_default > .location_detail > .txt_address')[0].text  # 주소
    print('ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ')
    call_rows = soup.selct('.location_detail > .location_present > .num_contact > .txt_contact')[0].text  # 번호
    time_rows = soup.selct('.location_present > .list_operation > .li > .txt_operation')[0].text  # 영업시간(덩어리큰것)
    update_rows = soup.selct('.info_revise > .date_revise')[0].text  # 업뎃날짜

    # sheet1.append([tit_rows, "", addr_rows, "", call_rows, time_rows, update_rows])
'''