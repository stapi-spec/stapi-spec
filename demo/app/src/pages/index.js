import Head from 'next/head';

import Layout from '@components/Layout';
import Section from '@components/Section';
import Container from '@components/Container';
import Map from '@components/Map';
import Button from '@components/Button';

import styles from '@styles/Home.module.scss';

const DEFAULT_CENTER = [38.907132, -77.036546];
const DEFAULT_ZOOM = 3;

export default function Home() {

  return (
    <Layout>
      <Head>
        <title>Task a Satellite</title>
        <meta name="description" content="Sat Tasking Sprint Front End Demo" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container>
        <Map
          className={styles.homeMap}
          width="800"
          height="400"
          center={DEFAULT_CENTER}
          zoom={DEFAULT_ZOOM}
          minZoom={2}
          maxZoom={20}
        />

        <p className={styles.description}>
          <code className={styles.code}>
            yarn create next-app -e
            https://github.com/colbyfayock/next-leaflet-starter
          </code>
        </p>

        <p className={styles.view}>
          <Button href="https://github.com/Element84/sat-tasking-sprint">
            Vew on GitHub
          </Button>
        </p>
      </Container>
    </Layout>
  );
}
