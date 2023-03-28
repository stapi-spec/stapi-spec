import { createContext, useContext, useState } from "react";

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
  return (
    <AppContext.Provider value={app}>
      {children}
    </AppContext.Provider>
  )
}

export function useAppContext() {
  return useContext(AppContext);
}
