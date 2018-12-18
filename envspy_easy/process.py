import json
import numpy as np
import pandas as pd


def main():   
    with open('20181218.json', 'r', encoding='gbk') as f:
        histaqi = json.load(f)
    res = retrieve_data(histaqi)
    print('done 111111111111111')
    res = retrieve_data(histaqi, prov_name = '热门城市')
    print('done 222222222222222')
    res = retrieve_data(histaqi, prov_name = '热门城市', city_name = '成都 ')
    # print(res)
    print('done 333333333333333')
    exit(0)
    for prov_name, prov_data in histaqi.items():
        print(prov_name)
        for city_name, city_data in prov_data.items():
            print(city_name)
            result = fetch_data(city_data)
            print(result)


def retrieve_data(histaqi, prov_name = None, city_name = None):
    try:
        print('trying')
        if city_name:
            city_data = histaqi[prov_name][city_name]
            results = fetch_data(city_data)
            print('if is ok')
        else:
            results = {}
            for city_name, city_data in histaqi[prov_name].items():
                print(city_name)
                result = fetch_data(city_data)
                results[city_name] = result  
            print('else is ok')     
    except Exception as identifier:
        print(identifier)
        results = {}
        for prov_name, prov_data in histaqi.items():
            print(prov_name)
            results[prov_name] = {}
            for city_name, city_data in prov_data.items():
                print(city_name)
                result = fetch_data(city_data)
                results[prov_name][city_name] = result
        print('whoops an exception')
    else:
        print(prov_name + " is done.")
    finally:
        return results


def fetch_data(city_data):
    result = []
    for val in city_data.values():
        result.extend(val)
    result = np.array(result).reshape(-1, 9)
    result = pd.DataFrame(result, columns = ['Date', 'aqi', 'aqi-rank', \
                'pm25', 'pm10', 'so2', 'no2', 'co', 'o3']).set_index('Date')

    return result

if __name__ == "__main__":
    main()