import { createContext, useContext, useEffect, useState } from "react";

const AppContext = createContext();

export default function AppProvider({ children }) {
  const today = new Date();
  const [geoJson, setGeoJson] = useState();
  const [dateRange, setDateRange] = useState([today, today.getDate() + 7]);
  const app = {
    geoJson,
    setGeoJson,
    dateRange,
    setDateRange
  }

  useEffect(()=>{
    if(!!geoJson) {
      console.log('make request to /pineapple');
    }
  }, [geoJson, dateRange]);

  return (
    <AppContext.Provider value={app}>
      {children}
    </AppContext.Provider>
  )
}

export function useAppContext() {
  return useContext(AppContext);
}
