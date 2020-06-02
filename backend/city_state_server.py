import flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin
import json
import create_city_state



app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r'/*': {"origins": "*"}})


state_dict, county_dict, city_dict = create_city_state.setup_maps()
cities_detail_data = create_city_state.get_all_cities_data()



def get_city_state_data():
    # state_d, state_county_d, state_county_city_d = create_city_state.setup_maps()
    return create_city_state.setup_maps()


def getData():
    books = [
        {'id':0,
         'title':'A fire Upon the Deep',
         'author': 'Vernor Vinge',
         'first_sentence': 'The cold Sleep itself was dreamless.',
         'year_publish':'1992'},
        {'id': 1,
         'title': 'The ones who walk away from Momleas',
         'author': 'Mary',
         'first_sentence': 'This is first sentences from Mary.',
         'year_publish': '1975'},
        {'id': 2,
         'title': 'The this the third book',
         'author': 'Karen',
         'first_sentence': 'Third book, This is first sentences from Karen.',
         'year_publish': '1995'}
    ]
    return books

@app.route('/', methods=['GET'])
def home():
    return "<h1> Flask Server</h> <p> A simple server for City State app developments <p>"

@app.route('/api/get_all_data')
def api_all():
    return jsonify([state_dict, county_dict, city_dict])
    # # obj = get_city_state_data()
    # return jsonify([o for o in obj])
    # return jsonify(getData())


@app.route('/api/get_all_city_data')
def api_all_city_data():
    return jsonify(cities_detail_data)
    # obj = get_city_state_data()
    # return jsonify([o for o in obj[0]])
    # return jsonify(getData())



@app.route('/api/get_states')
def api_all_states():
    return jsonify([k for k in state_dict])
    # obj = get_city_state_data()
    # return jsonify([o for o in obj[0]])
    # return jsonify(getData())


@app.route('/api/get_county', methods=['GET', 'POST'])
def api_get_county():
    if request.method == 'GET':
        print('request.args:', request.args)
        payload = request.args
    else:
        print('request:', request.data)
        print('request json:', request.get_json())
        payload = request.get_json()
        if payload is None:
            print('json is not available .. convert dta string to json')
            payload = json.loads(request.data)

    if 'state' in payload:
        input_state = payload['state']
        print('input state = ', input_state)
    else:
        return "Error , no id field provide, please speficy an id"

    if input_state in county_dict:
        results = [c for c in county_dict[input_state]]
        return jsonify(county_dict[input_state])
    else:
        return jsonify(['state: '+input_state+' not found'])

@app.route('/api/get_city', methods=['GET', 'POST'])
def api_get_city():
    if request.method == 'GET':
        print('request.args:', request.args)
        payload = request.args
    else:
        print('request:', request.data)
        print('request json:', request.get_json())
        payload = request.get_json()
        if payload is None:
            print('json is not available .. convert dta string to json')
            payload = json.loads(request.data)

    if 'state' in payload and 'county' in payload:
        input_state = payload['state']
        input_county = payload['county']
        print('input state = ', input_state, 'input county =', input_county)
    else:
        return jsonify("Error , need state and county ")

    if input_state not in city_dict :
        return jsonify("state :"+input_state+" not defined ")
    elif input_county not in city_dict[input_state]:
        return jsonify(" county: "+input_county+" not defined in state: "+input_state)
    return jsonify(city_dict[input_state][input_county])




@app.route('/api/get_city_data', methods=['GET', 'POST'])
def api_get_city_data():
    if request.method == 'GET':
        print('request.args:', request.args)
        payload = request.args
    else:
        print('request:', request.data)
        print('request json:', request.get_json())
        payload = request.get_json()
        if payload is None:
            print('json is not available .. convert dta string to json')
            payload = json.loads(request.data)

    if 'state' in payload and 'county' in payload and 'city' in payload:
        input_state = payload['state']
        input_county = payload['county']
        input_city = payload['city']
        print('input state = ', input_state, 'input county =', input_county, 'input city =', input_city)
    else:
        return jsonify("Error , need state and county ")

    if input_state not in cities_detail_data :
        print (cities_detail_data.keys())
        return jsonify("state :"+input_state+" not defined ")
    elif input_county not in cities_detail_data[input_state]:
        return jsonify(" county: "+input_county+" not defined in state: "+input_state)
    elif input_city not in cities_detail_data[input_state][input_county]:
        print('state:', input_state, 'county:', input_county, 'cities=', cities_detail_data[input_state][input_county].keys())
        return jsonify(" city: "+input_city+" not defined in state: "+input_state + " and county: "+input_county)
    return jsonify(cities_detail_data[input_state][input_county][input_city])



@app.route('/api/get_tmp', methods=['GET', 'POST'])
def api_get_tmp():
    # check if an ID is provide as part of the URL
    # if yes, assign it to a variable
    # if no, display an error
    if request.method == 'GET':
        print('request.args:', request.args)
        payload = request.args
    else:
        print('request:', request.data)
        print('request json:', request.get_json())
        payload = request.get_json()
        if payload is None:
            print('json is not available .. convert dta string to json')
            payload = json.loads(request.data)

    if 'state' in payload:
        input_state = payload['state']
        print('input state = ', input_state)
    else:
        return "Error , no id field provide, please speficy an id"

    if 'id2' in payload:
        id2 = int(payload['id2'])
        print('id2= ', id2)

    books = getData()
    results = []

    for book in books:
        if 'id' in payload and book['id'] == id1:
            results.append(book)
        if 'id2' in payload and book['id'] == id2:
            results.append(book)

    return jsonify(results)


if __name__ == "__main__":
    print('start server ...')
    app.run(host="0.0.0.0", debug=True, port=8300)
