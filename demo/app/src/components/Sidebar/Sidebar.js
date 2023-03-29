import RingLoader from 'react-spinners/RingLoader';
import Button from '@components/Button';
import {
  HorizontalSlidersLines,
  AlignJustifyDown,
} from '@vectopus/atlas-icons-react';
import styles from "./Sidebar.module.scss";

import { useAppContext } from 'src/context/appContext';
import OpportunityList from './OpportunityList';

export default function Sidebar(props) {
  const { isLoading, error, openFilters, setOpenFilters } = useAppContext();
  const filterButtonClass = openFilters
    ? styles.filterButtonOpen
    : styles.filterButtonClosed

  return (
    <div className={styles.sidebar}>
      {!isLoading && !error && (
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
          <OpportunityList/>
          {!!openFilters && (
            <div className={styles.filtersFlyout}>
              <div className={styles.filtersTopBar}>
                <h4>Filters</h4>
              </div>
            </div>
          )}
        </>
      )}
      {!!isLoading && !error && (
        <div className={styles.loader}>
          <RingLoader color="#5fbb9d" />
        </div>
      )}
      {!!error && <div>There was error</div>}
    </div>
  );
}
