import RingLoader from 'react-spinners/RingLoader';
import Button from '@components/Button';
import styles from './Sidebar.module.scss'

import { useAppContext } from 'src/context/appContext';
import OpportunityList from './OpportunityList';

export default function Sidebar(props) {
  const { isLoadingOpps, errorOpps } = useAppContext();
  return (
    <div className={styles.sidebar}>
      {!isLoadingOpps && !errorOpps &&(<div>
        <div className={styles.sidebarHeader}>
          <h2>Opportunities</h2>
          <Button></Button>
        </div>
        <OpportunityList />
      </div>)}
      {!!isLoadingOpps && !errorOpps && (
        <div className={styles.loader}><RingLoader color="#5fbb9d"/></div>
      )}
      {!!errorOpps && (
        <div>There was error</div>
      )}
    </div>
  );
}
