import json
import numpy as np
import pandas_market_calendars as mcal

def get_2yr_buz_days():
    nyse = mcal.get_calendar('NYSE')
    aa = nyse.valid_days(start_date='2018-05-01', end_date='2020-05-31')
    return list(aa.strftime('%Y-%m-%d'))


def get_state():
    state={'NY':5, 'NJ':4, 'CT':6}
    return state


def _set_county(state, num_county):
    # return {state:state+"_county"+str(i)for i in range(num_county)}
    return [state+"_county"+str(i)for i in range(num_county)]


def set_county(states):
    state_county_map = dict()
    for state in states:
        number = states[state]
        state_county_map[state] =_set_county(state, number)
    return state_county_map


def _set_city(state, county, num_city=3):
#    return {county:county+"_city_0"+str(i)for i in range(num_city)}
    return [state+"_"+county+"_city_0"+str(i)for i in range(num_city)]


def set_city(state_county_map):
    state_county_city = dict()
    for state in state_county_map:
        state_county_city[state] = dict()
        for county in state_county_map[state]:
            state_county_city[state][county] = _set_city(state, county, 3)
    return state_county_city


def get_int_range(sz, maxdist):
    while True:
        x,y = sorted(list(np.random.randint(0,sz,2)))
        if y - x > maxdist:
            break
    return x,y


def set_one_city_data():
    buzDate=get_2yr_buz_days()   # total 524 days
    category = ['market perform', 'sector perform', 'underperform', 'nutural']
    sz = np.random.randint(400,500)
    x = np.random.random(sz)
    y = np.random.random(sz) + np.random.randint(3,8)
    d = buzDate[-sz:]

    ans = []
    X = [[d[i], x[i]] for i in range(sz)]
    Y = [[d[i], y[i]] for i in range(sz)]
    ans.append({'oas': X})
    ans.append({'ref1': Y})

    if np.random.rand() > 0.3:  # get ref 2
#        print('create ref2, randint(0,sz):', sz)
        t1, t2 = get_int_range(sz, int(sz * 0.1))
        print('create ref2, t1, t2:', t1, t2)
        z2 = np.random.random(sz) + np.random.randint(3, 8)
        Z2 = [[d[i], z2[i]] for i in range(t1, t2)]
        ans.append({'ref2': Z2})
        if np.random.rand() > 0.3:  # get ref 3
            print('create ref3, randint(0,sz):', sz)
            t1, t2 = get_int_range(sz, int(sz * 0.1))
            print('create ref3, t1, t2 :', t1, t2)
            z3 = np.random.random(sz) + np.random.randint(3, 8)
            Z3 = [[d[i], z3[i]] for i in range(t1, t2)]
            ans.append({'ref3': Z3})


    markerSz = max(0, np.random.randint(-2,5))
    print ("sz:", sz, "markerSZ:", markerSz)
    markers = []
    for i in range(markerSz):
        dd = np.random.randint(sz) -1
        idx = np.random.randint(4)
        markers.append([X[dd][0], X[dd][1], category[idx]])
    ans.append({'label':markers})

    return ans




    # return [list(x),list(y)]


def get_all_cities_data():
    stateMap, state_county, state_county_city = setup_maps()
    data = dict()
    np.random.seed(1)
    for state in state_county_city:
        data[state] = dict()
        for county in state_county_city[state]:
            data[state][county] = dict()
            for city in state_county_city[state][county]:
                data[state][county][city] = set_one_city_data()
    return data


#     county_dict = set_county()
#     for state in states:
#         counties = get_counties(state, county_dict)
#         for city in set_



def get_counties(state, countyDict):
    return countyDict[state]


def get_cities(state, city, cityDict):
    return cityDict[state][city]

def setup_maps():
    stateMap = get_state()
    state_county = set_county(stateMap)
    state_county_city = set_city(state_county)
    return stateMap, state_county, state_county_city


if __name__ == "__main__":
    state_d, state_county_d, state_county_city_d = setup_maps()
    input_st = input('what is the state'+" ".join(list(state_d.keys()))+" ")
    input_cnty = input('what is the county'+ " ".join(list(state_county_city_d[input_st]))+" ")
    print('output city:', " ".join(state_county_city_d[input_st][input_cnty]))

    print('finish')

#
#
# stateDict = get_state()
# st = input('what is the state'+" ".join(list(stateDict.keys()))+" ")
# print('state = ', st)
#
# cntyDict = set_county(st, stateDict[st])
#
# pass




