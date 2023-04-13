import { createContext, useContext, useRef, useMemo, useState } from 'react';
import useGetOpportunities from 'src/hooks/useGetOpportunities';
import useGetProducts from '../hooks/useGetProducts';
import { formatToISOString } from 'src/utils';

const AppContext = createContext();

const today = new Date();
const defaultUserParams = {
  dateRange: [
    today,
    new Date(new Date(today).setDate(today.getDate() + 3)),
  ],
  provider: 'all',
  product: 'all'
}

export default function AppProvider({ children }) {
  /**
   * @typedef {object} UserParams
   * @property {[Date, Date]} dateRange
   * @property {number[]} [geometry]
  */
  /** @type {[UserParams, Function]} */
  const [
    userParams,
    setUserParams
  ] = useState({...defaultUserParams});
  const [hoveredOpportunity, setHoveredOpportunity] = useState(null);
  const [selectedOpportunity, setSelectedOpportunity] = useState(null);
  const [openFilters, setOpenFilters] = useState(false);
  const opportunitiesRef = useRef(null);

  const postParams = useMemo(() => {
    return userParams.geometry ? {
        params: {
          "geometry": userParams.geometry,
          "datetime": formatToISOString(userParams.dateRange),
          "product_id": userParams.product
        },
        provider: userParams.provider
      } : null;
  }, [userParams])

  const { isLoading: isLoadingProducts, data: products, error: errorProducts } = useGetProducts();
  const { isLoading: isLoadingOpps, data: opportunitiesData, error: errorOpps } = useGetOpportunities(products, postParams);

  opportunitiesRef.current = (postParams && opportunitiesData) ? opportunitiesData : null;

  function resetSearch(){
    setUserParams({...defaultUserParams});
  }

  const app = {
    userParams,
    setUserParams,
    isLoadingOpps,
    isLoadingProducts,
    products,
    errorProducts,
    opportunities: opportunitiesRef.current,
    errorOpps,
    selectedOpportunity,
    setSelectedOpportunity,
    hoveredOpportunity,
    setHoveredOpportunity,
    openFilters,
    setOpenFilters,
    setHoveredOpportunity,
    resetSearch
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
