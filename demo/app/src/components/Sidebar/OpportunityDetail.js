import styles from './Sidebar.module.scss'
import { useAppContext } from 'src/context/appContext';
import Button from '@components/Button';
import {
  ArrowRightLine
} from '@vectopus/atlas-icons-react';

export default function OpportunityDetail() {
  const { selectedOpportunity, setSelectedOpportunity, setHoveredOpportunity } = useAppContext();
  return (
    <div className={styles.opportunityDetail}>
        <div className={styles.topBar}>
            <h3 className={styles.heading}>Tasking Request Details</h3>
            <Button
              className={`${styles.closeButton} ${styles.closeButtonDetail}`}
              onClick={() => {
                setSelectedOpportunity(null);
                setHoveredOpportunity(null);
            }}
            >
              <ArrowRightLine size={12} />
            </Button>
        </div>
        <ul className={styles.detailList}>
            <li>
                <h3>{'ID'}</h3>
                <p>{selectedOpportunity.id}</p>
            </li>
        {
            Object.keys(selectedOpportunity.properties).map(key => {
                return (
                    selectedOpportunity.properties[key] &&
                        <li>
                            <h3>{key}</h3>
                            <p>{key === 'datetime' ?
                                selectedOpportunity.properties[key].split('/').map(utc => {
                                    return new Date(utc).toLocaleString()
                                }).join(' - ') :
                                selectedOpportunity.properties[key]}
                            </p>
                        </li>
                )
            })
        }
        </ul>
    </div>
  );
}
