import RingLoader from 'react-spinners/RingLoader';
import Button from '@components/Button';
import {
  HorizontalSlidersLines,
  AlignJustifyDown,
  ArrowRightLine
} from '@vectopus/atlas-icons-react';
import styles from "./Sidebar.module.scss";

import { useAppContext } from 'src/context/appContext';
import OpportunityList from './OpportunityList';
import { useEffect, useState } from 'react';

export default function Sidebar(props) {
  const {
    opportunities,
    isLoadingOpps,
    errorOpps,
    openFilters,
    setOpenFilters,
    products,
    isLoadingProducts,
    isErrorProducts,
  } = useAppContext();
    console.log('🚀 ~ file: Sidebar.js:24 ~ Sidebar ~ products:', products)

  const filterButtonClass = openFilters
    ? styles.filterButtonOpen
    : styles.filterButtonClosed

  return (
    <div className={styles.sidebar}>
      {!isLoadingOpps && (
        <>
          <div className={styles.topBar}>
            <h3 className={styles.heading}>Opportunities</h3>
            <Button className={filterButtonClass} onClick={() => setOpenFilters(!openFilters)}>
              <HorizontalSlidersLines size={12} />
            </Button>
            <Button className={styles.sortButton}>
              Sort 
              <AlignJustifyDown size={12} className={styles.sortIcon} />
            </Button>
          </div>

          {!errorOpps && (
            <OpportunityList/>
          )}

          {!!errorOpps && <div>There was error</div>}
          
          {!!openFilters && (
            <div className={styles.filtersFlyout}>
              <div className={styles.filtersTopBar}>
                <h4>Filters</h4>
                <Button className={styles.closeButton} onClick={() => setOpenFilters(false)}>
                  <ArrowRightLine size={12} />
                </Button>
              </div>
              <div className={styles.filtersBody}>
                {products.length && (<select>
                  {products.map(({ title, id }) => {
                    return (<option key={id} value={id}>{title}</option>)
                  })}
                </select>)}
              </div>
            </div>
          )}
        </>
      )}
      {!!isLoadingOpps && !errorOpps && (
        <div className={styles.loader}>
          <RingLoader color="#5fbb9d" />
        </div>
      )}
    </div>
  );
}
