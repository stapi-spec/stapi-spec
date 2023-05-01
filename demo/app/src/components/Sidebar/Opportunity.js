import { formatToFriendlyString } from 'src/utils';
import styles from './Sidebar.module.scss';
import Image from 'next/image'

const imageIdToPath = {
  'earthsearch': '/EarthSearchLogo.jpg',
  'planet': '/PlanetLogo.png',
  'umbra': '/UmbraLogo.png',
  'blacksky': '/BlackSkyLogo.png'
}

export default function Opportunity({
    title,
    provider,
    start,
    end,
    selected,
    onMouseEnter,
    onMouseLeave,
    onClick
}) {
  return (
    <div
        className={`${styles.opportunityPreview} ${selected && styles.selected}`}
        onClick={onClick}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
      >
        <div className={styles.logoContainer}>
          <Image src={imageIdToPath[provider] ?? '/logo.png'} width='25' height='25' />
        </div>
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
