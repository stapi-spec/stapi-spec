import { createContext, useContext, useMemo, useState } from 'react';
import useApiRequest from 'src/hooks/useApiRequest';
import { formatToValidTuple, formatToISOString } from 'src/utils/mapUtils';

const AppContext = createContext();

export default function AppProvider({ children }) {
  const today = new Date();
  /**
   * @typedef {object} UserParams
   * @property {[Date, Date]} dateRange
   * @property {number[]} bbox
  */
  const [
    /** @type {UserParams} */ userParams,
    setUserParams
  ] = useState({
    dateRange: [
    today,
    new Date(new Date(today).setDate(today.getDate() + 7)),
  ]
  });
  const [selectedOpportunity, setSelectedOpportunity] = useState();

  const params = useMemo(() => {
    return userParams.bbox ? {
      "bbox": formatToValidTuple(userParams.bbox),
      "datetime": formatToISOString(userParams.dateRange)
      //start_date: dateRange[0], call time formatting here
      //end_date: dateRange[1] call time formatting here
    } : null;
  }, [userParams])

  const { isLoading, data: opportunities, error } = useApiRequest(params);

  const app = {
    userParams,
    setUserParams,
    isLoading,
    opportunities,
    error,
    selectedOpportunity,
    setSelectedOpportunity
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
