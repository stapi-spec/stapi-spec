import { createContext, useContext, useMemo, useState } from 'react';
import useGetOpportunities from 'src/hooks/useGetOpportunities';
import useGetProducts from '../hooks/useGetProducts';
import { formatToISOString } from 'src/utils';

const AppContext = createContext();

export default function AppProvider({ children }) {
  const today = new Date();
  /**
   * @typedef {object} UserParams
   * @property {[Date, Date]} dateRange
   * @property {number[]} [geometry]
  */
  /** @type {[UserParams, Function]} */
  const [
    userParams,
    setUserParams
  ] = useState({
    dateRange: [
      today,
      new Date(new Date(today).setDate(today.getDate() + 3)),
    ],
    provider: 'all',
    product: 'all'
  });
  const [hoveredOpportunity, setHoveredOpportunity] = useState(null);
  const [selectedOpportunity, setSelectedOpportunity] = useState(null);
  const [openFilters, setOpenFilters] = useState(false);

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
  const { isLoading: isLoadingOpps, data: opportunities, error: errorOpps } = useGetOpportunities(products, postParams);

  const app = {
    userParams,
    setUserParams,
    isLoadingOpps,
    isLoadingProducts,
    products,
    errorProducts,
    opportunities,
    errorOpps,
    selectedOpportunity,
    setSelectedOpportunity,
    hoveredOpportunity,
    setHoveredOpportunity,
    openFilters,
    setOpenFilters,
    setHoveredOpportunity
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
