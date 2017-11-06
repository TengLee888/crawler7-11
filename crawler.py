from bs4 import BeautifulSoup
import requests
import json


storeDetails = [] #門市資訊全存在這個array
url = "http://emap.pcsc.com.tw/EMapSDK.aspx"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'postman-token': "99d24f0e-1304-612f-9788-13d4cdfe18c9"
    }


# 全台25個城市
with open('data.json', 'r') as f:
    cities = json.load(f)


for i in range(0,25):
    areas = []
    cityID = cities[i]['cityID'] #request要用的資料
    city = cities[i]['city'] #request要用的資料
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"commandid\"\r\n\r\nGetTown\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"cityid\"\r\n\r\n" + cityID + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    response = requests.request("POST", url, data=payload, headers=headers) #form-data包含cityID的request，發出請求
    soup = BeautifulSoup(response.text, 'html.parser')   #得到城市裡的所有地區
    townNames = soup.find_all('townname') #過濾資料，得到所有<townname>地區名</townname>
    for townName in townNames:
        area = str(townName).replace('<townname>', '').replace('</townname>', '') #從 <townname>松山區</townname> 變為 '松山區'
        payloadArea = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"commandid\"\r\n\r\nSearchStore\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"city\"\r\n\r\n" + city +"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"town\"\r\n\r\n" + area + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        payloadEncode = payloadArea.encode('utf-8') #編譯城市名及地區名
        response2 = requests.request("POST", url, data=payloadEncode, headers=headers) #form-data包含城市名和地區名，發出請求
        soup2 = BeautifulSoup(response2.text, 'html.parser') #得到地區內所有7-11的資料
        stores = soup2.find_all('geoposition') # 把一長串程式碼變成list
        for store in stores:
            poiname = str(store.find('poiname')).replace('<poiname>', '').replace('</poiname>', '') #過濾店名
            address = str(store.find('address')).replace('<address>', '').replace('</address>', '') #過濾地址
            storeDetails.append({poiname , address})


print(storeDetails)
