import { createContext, useContext, useMemo, useState } from "react";
import useApiRequest from "src/hooks/useApiRequest";

const AppContext = createContext();

export default function AppProvider({ children }) {
  const today = new Date();
  const [geoJson, setGeoJson] = useState();
  const [bbox, setBbox] = useState();
  const [dateRange, setDateRange] = useState([
    today,
    new Date(today).setDate(today.getDate() + 7),
  ]);

  const params = useMemo(() => {
    return bbox ? {
      "bbox": formatToValidTuple(bbox),
      //start_date: dateRange[0], call time formatting here
      //end_date: dateRange[1] call time formatting here
    } : null;
  }, [bbox, /*dateRange*/])

  const { isLoading, data: opportunities, error } = useApiRequest(params);

  const app = {
    geoJson,
    setGeoJson,
    bbox,
    setBbox,
    dateRange,
    setDateRange,
    isLoading,
    opportunities,
    error
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

function formatToValidTuple(bbox){
  return [bbox._southWest.lat, bbox._southWest.lng, bbox._northEast.lat, bbox._northEast.lng];
}
