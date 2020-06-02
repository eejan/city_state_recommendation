import { configureStore } from '@reduxjs/toolkit';
import plotSliceReducer from '../features/plot/plotSlice';

export default configureStore({
  reducer: {
    plot: plotSliceReducer,
  },
});
