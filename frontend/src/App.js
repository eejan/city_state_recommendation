import React, {useEffect, useState} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import {plotSlice} from './features/plot/plotSlice';
import './App.css';
import axios from "axios";
import Highcharts from 'highcharts';
import HighChartsReact from 'highcharts-react-official';
require("highcharts/modules/annotations")(Highcharts);

const ALL_STATES_URL = 'http://localhost:8300/api/get_states';
const ALL_COUNTIES_URL = 'http://localhost:8300/api/get_county?'
const ALL_CITIES_URL = 'http://localhost:8300/api/get_city?';
const ALL_DATA_URL = 'http://localhost:8300/api/get_city_data?';

function App() {
    const store = useSelector(state => state).plot
    const dispatch = useDispatch();
    const [highchart_options, setHighchart_options] = useState({});

    function getData() {
        return dispatch => {
            axios.get(ALL_STATES_URL)
                .then(res => dispatch(plotSlice.actions.fillStates(res.data)))
                .catch(err => console.log(err))
        }
    }

    useEffect(() => {
        dispatch(getData());
    }, []);


    function handleSubmit(e) {
        // debugger;
        const build_series_helper = (x) => {
            let nname = Object.keys(x)[0];
            return {name: nname, data: x[nname].map( (y) => [Date.parse(y[0]), y[1]])}
        }
        const build_annotations_helper = (z) => {
            return {point: {xAxis: 0, yAxis: 0, x:Date.parse(z[0]), y:z[1]}, text: z[2]}
        }
        let options = {
            chart: {type: 'spline'},
            title: {text: "".concat(store.selectedState, "-", store.selectedCounty, " plot")},
            xAxis: { type: 'datetime', labels: {format: '{value:%Y-%b-%e}'}},
            yAxis: { title: {text: 'Nominal OAS'} },
            series: store.data.slice(0, store.data.length-1).map(build_series_helper),
            annotations: [ { labels: store.data[store.data.length -1]["label"].map(build_annotations_helper) } ]
        }
        // debugger;
        setHighchart_options(options)
        e.preventDefault()
    }

    const user_selection = (e) => {
        if (e.target.name === "state") {
            let selectedState = e.target.value;
            dispatch(plotSlice.actions.selectState(selectedState));
            if (store.selectedCounty !== "") {
                dispatch(plotSlice.actions.selectCounty(""));
                dispatch(plotSlice.actions.selectCity(""));
            };
            axios.get(ALL_COUNTIES_URL.concat("state=", selectedState))
                .then(res => dispatch(plotSlice.actions.fillCounties(res.data)))
                .catch(e => console.log(e));
        } else if (e.target.name === "county") {
            let selectedCounty = e.target.value;
            dispatch(plotSlice.actions.selectCounty(selectedCounty));
            if (store.selectedCity !== "") { dispatch(plotSlice.actions.selectCity("")) };
            axios.get(ALL_CITIES_URL.concat("state=", store.selectedState, "&county=", selectedCounty))
                .then(res => dispatch(plotSlice.actions.fillCities(res.data)))
                .catch(e => console.log(e));
        } else {
            let selectedCity = e.target.value;
            dispatch(plotSlice.actions.selectCity(selectedCity));
            let params = {"state":store.selectedState, "county":store.selectedCounty, "city":selectedCity}
            console.log(ALL_DATA_URL.concat(Object.keys(params).map(key => key + '=' + params[key]).join('&')));
            axios.get(ALL_DATA_URL.concat(Object.keys(params).map(key => key + '=' + params[key]).join('&')))
                .then(res => dispatch(plotSlice.actions.fillData(res.data)))
                .catch(e => console.log(e))
        }
    }

    return (
        <div className='content container-fluid'>
            <div className="App d-flex flex-row justify-content-center">
                <h1> Corporate Bond Recommender </h1>
            </div>
            <form className="d-flex flex-column" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="state"> Select a State </label>
                    <select className='form-control' value={store.selectedState} name="state" id="state" onChange={user_selection}>
                        <option disabled value=""></option>
                        {store.states.map(x => (
                            <option value={x}>{x}</option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="county"> Select a County </label>
                    <select className='form-control' disabled={store.selectedState === ""} name="county" id="county" value={store.selectedCounty}
                            onChange={user_selection}>
                        <option disabled value=""></option>
                        {store.counties && store.counties.map(x => (
                            <option value={x}>{x}</option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="city"> Select a City </label>
                    <select disabled={store.selectedCounty=== ""} className='form-control' name="city" id="city" value={store.selectedCity}
                            onChange={user_selection}>
                        <option disabled value=""></option>
                        {store.cities && store.cities.map(x => (
                            <option value={x}>{x}</option>
                        ))}
                    </select>
                </div>
                <div className="submit d-flex justify-content-center">
                    {store.selectedCity && (<button disabled={store.selectedCounty === "" || store.selectedState === "" || store.selectedCity === ""} type="submit"
                            value="submit" className="btn btn-primary mb-5">Submit
                    </button>)}
                </div>
            </form>
            <div className="d-flex flex-row plot-image justify-content-center">
                {highchart_options.series && (<HighChartsReact highcharts={Highcharts} constructortype={'stockChart'} options={highchart_options}/>)}
            </div>
        </div>
    )

}

export default App;
