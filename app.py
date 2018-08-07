from flask import Flask, request, jsonify
import json
import requests
import datetime, iso8601
import uuid
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/s20131533/WeatherBot-new-a64cb6a3a368.json'



my_id = uuid.uuid1()

app = Flask(__name__)



appKey = "1b4e36fb-2bb9-4380-8930-a63b1bfcefef"

# 현재 날씨(분별)
url_minutely = "https://api2.sktelecom.com/weather/current/minutely"

# 현재 날씨(시간별)
url_hourly = "https://api2.sktelecom.com/weather/current/hourly"

# 초단기 예보
url_forecast_3hours = 'https://api2.sktelecom.com/weather/forecast/3hours'

# 단기 예보
url_forecast_3days = 'https://api2.sktelecom.com/weather/forecast/3days'

# 중기 예보
url_forecast_6days = 'https://api2.sktelecom.com/weather/forecast/6days'


headers = {'Content-Type': 'application/json; charset=utf-8',
           'appKey': appKey}


#현재 날씨(분별)  api_index = 1
def minutely(weather):
    #print(weather)
    # 상대 습도
    humidity = weather['humidity']

    # 기압정보
    # 현지기압(Ps)
    pressure_surface  = weather['pressure']['surface']
    # 해면기압(SLP)
    pressure_seaLevel  = weather['pressure']['seaLevel']

    # 관측소
    # 관측소명
    station_name      = weather['station']['name']
    # 관측소 지점번호(stnid)
    station_id      = weather['station']['id']
    # 관측소 유형
    #- KMA: 기상청 관측소
    #- BTN: SKP 관측소
    station_type  = weather['station']['type']
    # 위도
    station_latitude  = weather['station']['latitude']
    # 경도
    station_longitude = weather['station']['longitude']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 현재기온
    temperature_tc = weather['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰유무(해당 격자 내)
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']

    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']
    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']

    # 강우정보
    # 1시간 누적 강우량
    rain_sinceOntime   = weather['rain']['sinceOntime']
    # 일 누적 강우량
    rain_sinceMidnight = weather['rain']['sinceMidnight']
    # 10분 이동누적 강우량
    rain_last10min     = weather['rain']['last10min']
    # 15분 이동누적 강우량
    rain_last15min     = weather['rain']['last15min']
    # 30분 이동누적 강우량
    rain_last30min     = weather['rain']['last30min']
    # 1시간 이동누적 강우량
    rain_last1hour     = weather['rain']['last1hour']
    # 6시간 이동누적 강우량
    rain_last6hour     = weather['rain']['last6hour']
    # 12시간 이동누적 강우량
    rain_last12hour    = weather['rain']['last12hour']
    # 24시간 이동누적 강우량
    rain_last24hour    = weather['rain']['last24hour']

    ret = '현재 기온 ' + temperature_tc + '\n최고 기온 ' + temperature_tmax + '\n최저 기온 ' + temperature_tmin + '\n하늘 상태 ' + sky_name + '\n풍속 ' + wind_wspd + '\n습도 ' + humidity

    return ret



#현재 날씨(시간별)     api_index = 2
def hourly(weather):
    # print(weather)
    # 상대 습도
    humidity     = weather['humidity']

    # 발표 시간
    timeRelease  = weather['timeRelease']

    # 격자정보
    # 위도
    grid_latitude  = weather['grid']['latitude']
    # 경도
    grid_longitude = weather['grid']['longitude']
    # 시, 도
    grid_city      = weather['grid']['city']
    # 시, 군, 구
    grid_county    = weather['grid']['county']
    # 읍, 면, 동
    grid_village   = weather['grid']['village']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc = weather['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰유무(해당 격자 내)
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']

    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']

    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']

    ret = '현재 기온 ' + temperature_tc + '\n최고 기온 ' + temperature_tmax + '\n최저 기온 ' + temperature_tmin + '\n하늘 상태 ' + sky_name + '\n풍속 ' + wind_wspd + '\n습도 ' + humidity

    return ret





# 단기 예보     api_index = 4
def forecast_3days(weather, date_time, date_diff):

    # 발표 시간
    timeRelease = weather['timeRelease']
    #print('발표 시간 : ' + timeRelease)



    second_diff = (datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(timeRelease,'%Y-%m-%d %H:%M:%S')).total_seconds()
    hour_diff = int(second_diff / 3600)


    if hour_diff < 3:
        temperature = weather['fcst3hour']['temperature']['temp4hour']
        wind_wspd = weather['fcst3hour']['wind']['wspd4hour']
        humidity = weather['fcst3hour']['humidity']['rh4hour']
        sky_name = weather['fcst3hour']['sky']['name4hour']
        precipitation_type = weather['fcst3hour']['precipitation']['type4hour']
        precipitation_prob = weather['fcst3hour']['precipitation']['prob4hour']

    elif (hour_diff + 1) % 3 == 1:
        temperature = weather['fcst3hour']['temperature']['temp' + str(hour_diff + 1) + 'hour']
        wind_wspd = weather['fcst3hour']['wind']['wspd' + str(hour_diff + 1) + 'hour']
        humidity = weather['fcst3hour']['humidity']['rh' + str(hour_diff + 1) + 'hour']
        sky_name = weather['fcst3hour']['sky']['name' + str(hour_diff + 1) + 'hour']
        precipitation_type = weather['fcst3hour']['precipitation']['type' + str(hour_diff + 1) + 'hour']
        precipitation_prob = weather['fcst3hour']['precipitation']['prob' + str(hour_diff + 1) + 'hour']

    elif hour_diff % 3 == 1:
        temperature = weather['fcst3hour']['temperature']['temp' + str(hour_diff) + 'hour']
        wind_wspd = weather['fcst3hour']['wind']['wspd' + str(hour_diff) + 'hour']
        humidity = weather['fcst3hour']['humidity']['rh' + str(hour_diff) + 'hour']
        sky_name = weather['fcst3hour']['sky']['name' + str(hour_diff) + 'hour']
        precipitation_type = weather['fcst3hour']['precipitation']['type' + str(hour_diff) + 'hour']
        precipitation_prob = weather['fcst3hour']['precipitation']['prob' + str(hour_diff) + 'hour']

    elif (hour_diff - 1) % 3 == 1:
        temperature = weather['fcst3hour']['temperature']['temp' + str(hour_diff - 1) + 'hour']
        wind_wspd = weather['fcst3hour']['wind']['wspd' + str(hour_diff - 1) + 'hour']
        humidity = weather['fcst3hour']['humidity']['rh' + str(hour_diff - 1) + 'hour']
        sky_name = weather['fcst3hour']['sky']['name' + str(hour_diff - 1) + 'hour']
        precipitation_type = weather['fcst3hour']['precipitation']['type' + str(hour_diff - 1) + 'hour']
        precipitation_prob = weather['fcst3hour']['precipitation']['prob' + str(hour_diff - 1) + 'hour']






    # 오늘
    if date_diff == 0:
        temperature_tmax = weather['fcstdaily']['temperature']['tmax1day']
        temperature_tmin = weather['fcstdaily']['temperature']['tmin1day']

    # 내일
    elif date_diff == 1:
        temperature_tmax = weather['fcstdaily']['temperature']['tmax2day']
        temperature_tmin = weather['fcstdaily']['temperature']['tmin2day']

    # 내일 모레
    elif date_diff == 2:
        temperature_tmax = weather['fcstdaily']['temperature']['tmax3day']
        temperature_tmin = weather['fcstdaily']['temperature']['tmin3day']

    else:
        temperature_tmax = '측정 불가'
        temperature_tmin = '측정 불가'



    if precipitation_type == '0':
        precipitation = '현상 없음'
    elif precipitation_type == '1':
        precipitation = '비'
    elif precipitation_type == '2':
        precipitation = '진눈깨비'
    elif precipitation_type == '3':
        precipitation = '눈'


    if precipitation_type == '0':
        period_ret ='최고 기온 ' + temperature_tmax + '\n최저 기온 ' + temperature_tmin + '\n하늘 상태 ' + sky_name + '\n강수 현상 없음'
    else:
        period_ret ='최고 기온 ' + temperature_tmax + '\n최저 기온 ' + temperature_tmin + '\n하늘 상태 ' + sky_name\
                            + '\n' + precipitation + ' 내릴 확률 ' + precipitation_prob + '%'




    if precipitation_type == '0':
        oneday_ret = '예상 기온 ' + temperature + '\n최고 기온 ' + temperature_tmax + '\n최저 기온 ' + temperature_tmin + '\n하늘 상태 ' + sky_name + '\n풍속 ' + wind_wspd \
                      + '\n습도 ' + humidity + '\n강수 현상 없음'
    else:
        oneday_ret = '예상 기온 ' + temperature + '\n최고 기온 ' + temperature_tmax + '\n최저 기온 ' + temperature_tmin + '\n하늘 상태 ' + sky_name + '\n풍속 ' + wind_wspd\
                  + '\n습도 ' + humidity + '\n' + precipitation + ' 내릴 확률 ' + precipitation_prob + '%'



    if category == 'period':
        return period_ret
    elif category == 'oneday':
        return oneday_ret
    elif category == 'continue':
        return oneday_ret



# 중기 예보     api_index = 5
def forecast_6days(weather,date_time):

    # 발표 시간
    timeRelease = weather['timeRelease']        # string type

    a = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')          # date type
    b = datetime.datetime.strptime(timeRelease, '%Y-%m-%d %H:%M:%S')        # date type

    days_diff = (a - b).days
    if days_diff < 2 or days_diff > 10:
        sky_name = '알 수 없음.'
    else:
        sky_name_am = weather['sky']['amName' + str(days_diff) + 'day']
        sky_name_pm = weather['sky']['pmName' + str(days_diff) + 'day']
        sky_name = '└오전 ' + sky_name_am + '\n└오후 ' + sky_name_pm

        tmax = weather['temperature']['tmax' + str(days_diff) + 'day']
        tmin = weather['temperature']['tmin' + str(days_diff) + 'day']



    text = weather['fcstextRegion']['text']

    detail_ret = text
    period_ret = '최고 기온 ' + tmax + '\n최저 기온 ' + tmin + '\n하늘 상태\n' + sky_name
    oneday_ret = '최고 기온 ' + tmax + '\n최저 기온 ' + tmin + '\n하늘 상태\n' + sky_name + '\n\n더 자세한 정보를 원하시면 "자세히" 라고 입력해주세요.'


    if category == 'period':
        return period_ret
    elif category == 'detail':
        return detail_ret
    elif category == 'oneday':
        return oneday_ret
    elif category == 'continue':
        return oneday_ret





def requestCurrentWeather(lat, lon, api_index, date_time, date_diff):
    if api_index == 5:
        params = { "version": "1",
                "lat" : lat,
                "lon" : lon,
                "foretxt" : "Y"}
    else:
        params = { "version": "1",
                "lat" : lat,
                "lon" : lon }


    if api_index == 1:
        response = requests.get(url_minutely, params=params, headers=headers)
    elif api_index == 2:
        response = requests.get(url_hourly, params=params, headers=headers)
    elif api_index == 3:
        response = requests.get(url_forecast_3hours, params=params, headers=headers)
    elif api_index == 4:
        response = requests.get(url_forecast_3days, params=params, headers=headers)
    elif api_index == 5:
        response = requests.get(url_forecast_6days, params=params, headers=headers)




    if response.status_code == 200:
        response_body = response.json()

        #날씨 정보
        try:
            if api_index == 1:
                weather_data = response_body['weather']['minutely'][0]

            elif api_index == 2:
                weather_data = response_body['weather']['hourly'][0]

            elif api_index == 3:
                weather_data = response_body['weather']['forecast3hours'][0]

            elif api_index == 4:
                weather_data = response_body['weather']['forecast3days'][0]

            elif api_index == 5:
                weather_data = response_body['weather']['forecast6days'][0]



            if api_index == 1:
                #print(minutely(weather_data))
                return minutely(weather_data)

            elif api_index == 2:
                #print(hourly(weather_data))
                return hourly(weather_data)

            elif api_index == 4:
                #print(forecast_3days(weather_data, date_time, date_diff))
                return forecast_3days(weather_data, date_time, date_diff)

            elif api_index == 5:
                #print(forecast_6days(weather_data, date_time))
                return forecast_6days(weather_data, date_time)

        except:
            pass
    else:
        pass
        #에러




#@app.route('/', methods=['GET', 'POST'])
@app.route('/webhook', methods=['GET', 'POST'])
def weather_request():

    global category
    global dayString
    dayString = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']


    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))

        #print(data)

        queryResult = data['queryResult']
        confidence = queryResult['intentDetectionConfidence']

        intent = queryResult['intent']
        parameters = queryResult['parameters']
        queryText = queryResult['queryText']
        fulfillmentText = None







        # 'weather' intent인 경우
        if intent['displayName'] == 'weather':

            today_str = datetime.datetime.now().strftime('%Y-%m-%d 12:00:00')  # string type
            today = datetime.datetime.strptime(today_str, '%Y-%m-%d %H:%M:%S')  # date type

            api_index = 4  # 단기예보 api 호출 (초기 설정)



            # "이번주 주말 논현 날씨", "다음주 날씨" 같이 범위로 물어본 경우
            if ('이번주' in queryText or '다음주' in queryText) and '요일' not in queryText:

                category = 'period'

                startDateTime_date = parameters['date-time']['startDateTime'][0:10]
                startDateTime_time = parameters['date-time']['startDateTime'][11:19]
                startDateTime_str = startDateTime_date + ' ' + startDateTime_time  # string type
                startDateTime = datetime.datetime.strptime(startDateTime_str, '%Y-%m-%d %H:%M:%S')  # date type

                endDateTime_date = parameters['date-time']['endDateTime'][0:10]
                endDateTime_time = parameters['date-time']['endDateTime'][11:19]
                endDateTime_str = endDateTime_date + ' ' + endDateTime_time  # string type
                endDateTime = datetime.datetime.strptime(endDateTime_str, '%Y-%m-%d %H:%M:%S')  # date type

                city = parameters['city']  # 예 - '서울시'
                country = parameters['country']  # 예 - '강남구'
                village = parameters['village']  # 예 - '논현동'

                if '이번주' in queryText and '주말' not in queryText:
                    startDateTime = datetime.datetime.strptime(today_str, '%Y-%m-%d %H:%M:%S')  # date type


            # "이번주 수요일 방배 날씨", "내일 잠원 날씨" 같이 하루만 콕 찝어서 물어본 경우
            else:

                category = 'oneday'

                date = parameters['date-time']['date_time'][0:10]  # 예 - '2018-07-23'
                time = parameters['date-time']['date_time'][11:19]  # 예 - '11:00:00'

                city = parameters['city']  # 예 - '서울시'
                country = parameters['country']  # 예 - '강남구'
                village = parameters['village']  # 예 - '논현동'



                if '현재' in queryText or '지금' in queryText:
                    api_index = 1  # 현재날씨(분별) api 호출

                # 날짜에 대한 정보가 안들어왔으면 '오늘 날짜'를 default로 설정
                if date == '':
                    date = today_str[0:10]
                    api_index = 1  # 현재날씨(분별) api 호출

                # 시간에 대한 정보가 안들어왔으면 '현재 시간'을 default로 설정
                if time == '':
                    time = datetime.datetime.now().strftime('%H:%M:%S')

                # '2018-07-20 14:22:22' 같은 형식
                date_time_str = date + ' ' + time  # string type

                second_diff = (
                            datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(
                        today_str, '%Y-%m-%d %H:%M:%S')).total_seconds()
                hour_diff = int(second_diff / 3600)

                print('시간 차이 : ' + str(hour_diff))

                today_hour = int(today_str[11:13])
                date_diff = int((today_hour + hour_diff) / 24)  # 0이면 오늘, 1이면 내일, 2면 내일모레
                print('날짜 차이 : ' + str(date_diff))

                # 2일 이상 차이나는 날짜에 대해서는 "중기 예보 api" 적용
                if date_diff >= 3:
                    api_index = 5





            # 위치에 대한 정보가 아무것도 안들어왔으면 '대흥동'을 default로 설정
            if city == '' and country == '' and village == '':
                location = '대흥동'
            elif village != '':
                location = village
            elif country != '':
                location = country
            elif city != '':
                location = city




            # 요청 주소(구글맵)
            URL = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address=' + location + '&key=AIzaSyCM1y3m25eC35UPyvI4MMcoMVqp4L9L560'

            # URL로 보낸 Requst의 Response를 response 변수에 할당
            response = requests.get(URL)

            # JSON 파싱
            data = response.json()

            # lat, lon 추출
            lat = data['results'][0]['geometry']['location']['lat']
            lon = data['results'][0]['geometry']['location']['lng']
            print('위도 : ' + str(lat))
            print('경도 : ' + str(lon))

            # 전체 주소 추출
            full_addr = data['results'][0]['formatted_address'][5:]     # '대한민국' 빼고
            print('전체 주소 : ' + full_addr)

            fulfillmentText = full_addr + '\n\n'



            # "이번주 주말 날씨", "다음주 날씨" 같이 범위로 물어본 경우
            if ('이번주' in queryText or '다음주' in queryText) and '요일' not in queryText:

                # 시작일부터 끝나는 날까지 반복하며 날씨 정보를 fulfillmentText에 붙여준다.
                # curDateTime은 현재 가리키고 있는 날짜
                curDateTime = startDateTime
                while curDateTime <= endDateTime:

                    # 오늘(날씨 발표일) 과의 일수 차이
                    days_diff = (curDateTime - today).days
                    if days_diff >= 3:
                        api_index = 5

                    curDateTime_str = curDateTime.strftime('%Y-%m-%d %H:%M:%S')

                    year = curDateTime.strftime('%Y')
                    month = curDateTime.strftime('%m')
                    day = curDateTime.strftime('%d')
                    weekday = dayString[datetime.date(int(year), int(month), int(day)).weekday()]

                    temp = '[' + month + '월 ' + day + '일 ' + weekday + ']\n' + requestCurrentWeather(lat, lon, api_index, curDateTime_str, days_diff)
                    fulfillmentText = str(fulfillmentText) + temp
                    fulfillmentText = str(fulfillmentText) + '\n\n====================\n\n'

                    day_1 = datetime.timedelta(days=1)
                    curDateTime = curDateTime + day_1



            # "이번주 수요일 방배 날씨", "내일 잠원 날씨" 같이 하루만 콕 찝어서 물어본 경우
            else:
                year = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y')
                month = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m')
                day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d')
                weekday = dayString[datetime.date(int(year), int(month), int(day)).weekday()]


                print('api index : ' + str(api_index))

                fulfillmentText = fulfillmentText + '[' + month + '월 ' + day + '일 ' + weekday + ' ' + time + ']\n'\
                                  + requestCurrentWeather(lat, lon, api_index, date_time_str, date_diff)



        # 'weather_detail' intent 인 경우
        elif intent['displayName'] == 'weather_detail':
            date_new = ''
            category = 'detail'

            date_original = parameters['date_original']['date_time'][0:10]  # 예 - '2018-07-23'
            time_original = parameters['date_original']['date_time'][11:19]  # 예 - '11:00:00'
            date_time_original_str = date_original + ' ' + time_original


            if parameters['date_new'] != '':
                date_new = parameters['date_new']['date_time'][0:10]
                time_new = parameters['date_new']['date_time'][11:19]
                date_time_new_str = date_new + ' ' + time_new


            city = parameters['city']  # 예 - '서울시'
            country = parameters['country']  # 예 - '강남구'
            village = parameters['village']  # 예 - '논현동'


            # 위치에 대한 정보가 아무것도 안들어왔으면 '대흥동'을 default로 설정
            if city == '' and country == '' and village == '':
                location = '대흥동'
            elif village != '':
                location = village
            elif country != '':
                location = country
            elif city != '':
                location = city


            # 요청 주소(구글맵)
            URL = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address=' + location + '&key=AIzaSyCM1y3m25eC35UPyvI4MMcoMVqp4L9L560'

            # URL로 보낸 Requst의 Response를 response 변수에 할당
            response = requests.get(URL)

            # JSON 파싱
            data = response.json()

            # lat, lon 추출
            lat = data['results'][0]['geometry']['location']['lat']
            lon = data['results'][0]['geometry']['location']['lng']


            # weather intent에서 바로 weather_detail intent로 가는 경우
            if date_new == '':
                fulfillmentText = requestCurrentWeather(lat, lon, 5, date_time_original_str, None)

            # weather intent에서 weather_continue intent 한번 거치고 weather detail intent로 가는 경우
            else:
                fulfillmentText = requestCurrentWeather(lat, lon, 5, date_time_new_str, None)





        # 'weather_continue' intent인 경우
        elif intent['displayName'] == 'weather_continue':

            category = 'continue'

            date_original = parameters['date_original']['date_time'][0:10]  # 예 - 2018-07-23
            time_original = parameters['date_original']['date_time'][11:19]  # 예 - 11:00:00

            city = parameters['city']  # 예 - 서울시
            country = parameters['country']  # 예 - 강남구
            village = parameters['village']  # 예 - 논현동

            api_index = 4  # 단기예보 api 호출 (초기 설정)



            date_new = parameters['date_new']['date_time'][0:10]
            time_new = parameters['date_new']['date_time'][11:19]





            today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            today_ver2 = datetime.datetime.now().strftime('%Y-%m-%d')

            if date_new == today_ver2:
                date_new = date_original



            # 날짜에 대한 정보가 안들어왔으면 '오늘 날짜'를 default로 설정
            if date_original == '':
                date_original = today[0:10]
                api_index = 1       # 현재날씨(분별) api 호출


            if date_new == '':
                date_new = date_original



            if '다음날' in queryText:
                day_1 = datetime.timedelta(days = 1)
                date_new = datetime.datetime.strptime(date_original, '%Y-%m-%d') + day_1
                date_new = date_new.strftime('%Y-%m-%d')




            # 시간에 대한 정보가 안들어왔으면 '현재 시간'을 default로 설정
            if time_original == '':
                time_original = datetime.datetime.now().strftime('%H:%M:%S')

            if time_new == '':
                time_new = time_original



            # '2018-07-20 14:22:22' 같은 형식
            date_time_new = date_new + ' ' + time_new



            second_diff = (datetime.datetime.strptime(date_time_new, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(today,'%Y-%m-%d %H:%M:%S')).total_seconds()
            hour_diff = int(second_diff / 3600)

            print('시간 차이 : ' + str(hour_diff))

            today_hour = int(today[11:13])
            date_diff = int((today_hour + hour_diff) / 24)  # 0이면 오늘, 1이면 내일, 2면 내일모레
            print('날짜 차이 : ' + str(date_diff))



            # 2일 이상 차이나는 날짜에 대해서는 "중기 예보 api" 적용
            if date_diff >= 3:
                api_index = 5




            # 위치에 대한 정보가 아무것도 안들어왔으면 '대흥동'을 default로 설정
            if city == '' and country == '' and village == '':
                location = '대흥동'
            elif village != '':
                location = village
            elif country != '':
                location = country
            elif city != '':
                location = city

            # 요청 주소(구글맵)
            URL = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address=' + location + '&key=AIzaSyCM1y3m25eC35UPyvI4MMcoMVqp4L9L560'

            # URL로 보낸 Requst의 Response를 response 변수에 할당
            response = requests.get(URL)

            # JSON 파싱
            data = response.json()

            # lat, lon 추출
            lat = data['results'][0]['geometry']['location']['lat']
            lon = data['results'][0]['geometry']['location']['lng']
            print('위도 : ' + str(lat))
            print('경도 : ' + str(lon))

            # 전체 주소 추출
            full_addr = data['results'][0]['formatted_address'][5:]     # '대한민국' 빼고
            print('전체 주소 : ' + full_addr)

            fulfillmentText = full_addr + '\n\n'



            year = datetime.datetime.strptime(date_new, '%Y-%m-%d').strftime('%Y')
            month = datetime.datetime.strptime(date_new, '%Y-%m-%d').strftime('%m')
            day = datetime.datetime.strptime(date_new, '%Y-%m-%d').strftime('%d')
            weekday = dayString[datetime.date(int(year), int(month), int(day)).weekday()]




            fulfillmentText = fulfillmentText + '[' + month + '월 ' + day + '일 ' + weekday + ' ' + time_new + ']\n'\
                              + requestCurrentWeather(lat, lon, api_index, date_time_new, date_diff)






        if not fulfillmentText:
            if 'fulfillmentText' in queryResult:
                fulfillmentText = queryResult['fulfillmentText']
            else:
                fulfillmentText = 'Default Response from Remote'


        result = {}
        result['fulfillmentText'] = fulfillmentText


        return jsonify(result)

    else:
        return 'GET method is used...'





@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type": "buttons",
        "buttons": ["어떻게 물어보면 될까?"]
    }

    return jsonify(dataSend)






@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()


    # 카카오톡에서 내가 입력한 값
    content = dataReceive['content']
    print('카톡에서 내가 입력한 말 : {}\n'.format(content))

    url = "https://kapi.kakao.com/v1/user/me"
    headers = {'Authorization' : 'Bearer 7f699333697115fcd80a5a41453c1888'}
    response = requests.request("POST", url, headers = headers)


    if content == u"어떻게 물어보면 될까?":
        dataSend = {
            "message": {
                "text": "<이런식으로 물어보세요>\n★오늘 날씨\n★논현동 날씨\n★내일 오후7시 잠원동 날씨\n★이번주 방배 날씨\n★이번주 주말 서초 날씨\n★다음주 날씨"
            }
        }
    else:
        dataSend = {
            "message" : {
                "text" : detect_intent_texts('weatherbot-new', my_id, content, 'ko')
            }
        }


    print('Data send : {}\n'.format(dataSend))

    return jsonify(dataSend)




def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""

    import dialogflow_v2 as dialogflow


    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)



    text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)




    response = session_client.detect_intent(session=session, query_input=query_input)




    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(response.query_result.intent.display_name,response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))
    #print(response.query_result)
    print('=' * 20)


    fulfillmentText = response.query_result.fulfillment_text


    return fulfillmentText





if __name__ == '__main__':
    #context = ('cert.crt', 'key.key')

    app.run(host='0.0.0.0', port=5003, debug=True, threaded=True)
