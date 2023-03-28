import AppProvider from 'src/context/appContext';
import '@styles/globals.scss';

function MyApp({ Component, pageProps }) {
  return <AppProvider><Component {...pageProps} /></AppProvider>
}

export default MyApp
