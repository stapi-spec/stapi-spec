import Link from 'next/link';
import { FaGithub } from 'react-icons/fa';
import DateRangePicker from '@wojtekmaj/react-daterange-picker/dist/DateRangePicker';

import { useAppContext } from 'src/context/appContext';
import Container from '@components/Container';

import styles from './Header.module.scss';

const Header = () => {
  const { dateRange, setDateRange } = useAppContext();

  return (
    <>
      <header className={styles.header}>
        <Container className={styles.headerContainer}>
          <p className={styles.headerTitle}>
            <Link href="/">
              {/* <Image src="/logo.png" alt="logo" width={35} height={35} /> */}
              Task a Satellite
            </Link>
          </p>
          <ul className={styles.headerLinks}>
            <li>
              <a href="https://github.com/Element84/sat-tasking-sprint" rel="noreferrer">
                <FaGithub />
              </a>
            </li>
          </ul>
        </Container>
      </header>
      <div className={styles.toolbar}>
        <DateRangePicker onChange={setDateRange} value={dateRange} clearIcon={null} minDate={new Date()} />
      </div>
    </>
  );
};

export default Header;
