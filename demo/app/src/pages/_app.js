import AppProvider from 'src/context/appContext';
import '@styles/globals.scss';

import '@styles/DateRangePicker.scss';
import 'react-calendar/dist/Calendar.css';

function MyApp({ Component, pageProps }) {
  return (
    <AppProvider>
      <Component {...pageProps} />
    </AppProvider>
  );
}

export default MyApp
