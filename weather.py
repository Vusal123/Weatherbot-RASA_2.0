import requests
from datetime import datetime, timedelta

def Weather(city,time): 
    print(city) #to see provided city data in command prompt
    print(time) #to see provided time data in command prompt
    degree_sign = u"\N{DEGREE SIGN}"
    api_key = "5e400ebbd6554a6f9b194637210705"
    api_address='http://api.weatherapi.com/v1/forecast.json?key=' + api_key + '&q='
    
    city_result = ''
    if type(city)==list:
        city_result = city[0]
    else:
        city_result = city
        
    url = api_address + city_result +'&days=3&aqi=no&alerts=no'
    json_data = dict(requests.get(url).json())

    #for the cases of not found city name"
    if 'error' in json_data:
        return 'Either the city name that you provided does not exist, or I did not understand you properly. Please start the query again and make sure that you have correct inputs'
    
    #time data is type dict
    if type(time)==dict:
        end = datetime(int(time['to'][:4]),int(time['to'][5:7]),int(time['to'][8:10]))
        start = datetime(int(time['from'][:4]),int(time['from'][5:7]),int(time['from'][8:10]))
        delta = end - start  # as timedelta
        days = [start + timedelta(days=i) for i in range(delta.days + 1)]
        all_days ='Weather condition for ' + city_result
        for j in days[:-1]:
            date_found = False
            required_date = str(j)[:10]
            for i in json_data['forecast']['forecastday']:
                if i['date']==required_date:
                    date_found=True
                    result = '  - max temp: ' + str(i['day']['maxtemp_c'])+ degree_sign + 'C\n  - min temp: ' + str(i['day']['mintemp_c'])+ degree_sign + 'C\n  - Expected Condition:' + i['day']['condition']['text']
                    all_days = all_days + '\n* ' + i['date'] +':\n' + result
            if date_found == False:
                if all_days == 'Weather condition for ' + city_result:
                    all_days = 'Sorry I am able to provide weather condition only for today and the next two days'
                else:
                    all_days = all_days + '\nSorry, I am not able to provide the weather condition for other requested days. I can provide only for today and next two days'
                break
        return all_days

    #time data is is type list
    elif type(time)==list:
        all_days ='Weather condition for ' + city_result
        not_found_days = ''
        for t in time:
            date_found = False
            required_date = str(t)[:10]
            for d in json_data['forecast']['forecastday']:
                if d['date']==required_date:
                    date_found=True
                    result = '  - max temp: ' + str(d['day']['maxtemp_c'])+ degree_sign + 'C\n  - min temp: ' + str(d['day']['mintemp_c'])+ degree_sign + 'C\n  - Expected Condition:' + d['day']['condition']['text']
                    all_days = all_days + '\n* ' + d['date'] +':\n' + result
            if date_found == False:
                not_found_days = not_found_days + '\n' + required_date
        if not_found_days != '':
            all_days = all_days + '\n' + 'I am able to provide weather condition only for today and the next two days. Sorry, I cannot provide weather condition for below requested dates:' + not_found_days
        return all_days  

    #time data is type str
    else:
        date_found = False    
        for i in json_data['forecast']['forecastday']:
            if i['date']==time[:10]:
                date_found=True
                result = 'Weather condition for ' + city_result + ':\n* ' + i['date'] +  ':\n  - max temp: ' + str(i['day']['maxtemp_c']) + degree_sign + 'C\n  - min temp: ' + str(i['day']['mintemp_c']) + degree_sign + 'C\n  - Expected Condition:' + i['day']['condition']['text']
                return result
        if date_found == False:
            return 'Sorry, I am able to provide the weather condition only for today and the next two days'