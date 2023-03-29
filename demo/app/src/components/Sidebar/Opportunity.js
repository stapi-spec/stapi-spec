import { formatToFriendlyString } from 'src/utils';
import styles from './Sidebar.module.scss'

export default function Opportunity({
    title,
    start,
    end
}) {
  return (
    <div className={styles.opportunityPreview}>
        <h1>{title}</h1>
        <div className={styles.previewStartDate}>
            {formatToFriendlyString(start) ?? 'no start date given'}
        </div>
        <div className={styles.previewEndDate}>
            {formatToFriendlyString(end) ?? 'no end date given'}
        </div>
    </div>
  );
}
