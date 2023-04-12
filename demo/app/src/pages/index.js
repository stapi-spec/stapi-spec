import Head from 'next/head';

import Layout from '@components/Layout';
import Container from '@components/Container';
import Map from '@components/Map';
import Sidebar from '@components/Sidebar';

import styles from '@styles/Home.module.scss';

import { useAppContext } from 'src/context/appContext';


const DEFAULT_CENTER = [38.907132, -77.036546];
const DEFAULT_ZOOM = 3;

export default function Home() {
  const { isLoadingOpps, errorOpps, opportunities,  } = useAppContext();
  return (
    <Layout>
      <Head>
        <title>Task a Satellite</title>
        <meta name="description" content="Sat Tasking Sprint Front End Demo" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container className={styles.mapContainer}>
        {(isLoadingOpps || opportunities || errorOpps) && <Sidebar/>}
        <Map
          className={styles.homeMap}
          width="800"
          height="400"
          center={DEFAULT_CENTER}
          zoom={DEFAULT_ZOOM}
          minZoom={2}
          maxZoom={20}
        />
      </Container>
    </Layout>
  );
}
