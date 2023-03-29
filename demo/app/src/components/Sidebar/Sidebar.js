import RingLoader from 'react-spinners/RingLoader';
import Button from '@components/Button';
import styles from './Sidebar.module.scss'

import { useAppContext } from 'src/context/appContext';

export default function Sidebar(props) {
  const { isLoading, error } = useAppContext()
  return (
    <div className={styles.sidebar}>
      {!isLoading && !error &&(<div>
        <h2>Opportunities</h2>
        <Button></Button>
      </div>)}
      {!!isLoading && !error && (
        <div className={styles.loader}><RingLoader color="#5fbb9d"/></div>
      )}
      {!!error && (
        <div>There was error</div>
      )}
    </div>
  );
}
