import styles from './Sidebar.module.scss'
import { useAppContext } from 'src/context/appContext';
import Button from '@components/Button';

export default function OpportunityDetail() {
  const { selectedOpportunity, setSelectedOpportunity, setHoveredOpportunity } = useAppContext();

  return (
    <div className={styles.opportunityDetail}>
        <div className={styles.topBar}>
            <h3 className={styles.heading}>Detail</h3>
            <Button
              onClick={() => {
                setSelectedOpportunity(null);
                setHoveredOpportunity(null);
            }}
            >
              x
            </Button>
        </div>
        <div>{selectedOpportunity.id}</div>
    </div>
  );
}
