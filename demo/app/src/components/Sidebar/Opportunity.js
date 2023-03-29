import styles from './Sidebar.module.scss'

export default function Opportunity({
    key,
    title,
    start,
    end
}) {
  return (
    <div className={styles.opportunityPreview} key={key}>
        <h1>{title}</h1>
        <div className={styles.previewStartDate}>
            {start ?? 'no start date given'}
        </div>
        <div className={styles.previewEndDate}>
            {end ?? 'no end date given'}
        </div>
    </div>
  );
}
