import { createSlice } from '@reduxjs/toolkit';

export const plotSlice = createSlice({
  name: 'plot_data',
  initialState: {
    selectedState: "",
    selectedCounty: "",
    selectedCity: "",
    states: [],
    counties: [],
    cities: [],
    data: []
  },
  reducers: {
    selectState: (state, action) => {
      // Redux Toolkit allows us to write "mutating" logic in reducers. It
      // doesn't actually mutate the state because it uses the Immer library,
      // which detects changes to a "draft state" and produces a brand new
      // immutable state based off those changes
      state.selectedState = action.payload;
    },
    selectCounty: (state, action) => {
      state.selectedCounty = action.payload;
    },
    selectCity: (state, action) => {
      state.selectedCity = action.payload;
    },
    fillData: (state, action) => {
      state.data = action.payload;
    },
    fillStates: (state, action) => {
      state.states = action.payload;
    },
    fillCounties: (state, action) => {
      state.counties = action.payload;
    },
    fillCities: (state, action) => {
      state.cities = action.payload;
    }
  },
});

export const { selectState, selectCounty, fill_data } = plotSlice.actions;

// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.plot.value)`
export const stateSelected = state => state.selectedState;
export const countySelected = state => state.selectedCounty;
export const citySelected = state => state.selectedCity;
export const data = state => state.data;
export const states = state => state.states;
export const counties = state => state.counties;
export const cities = state => state.cities;

export default plotSlice.reducer;
