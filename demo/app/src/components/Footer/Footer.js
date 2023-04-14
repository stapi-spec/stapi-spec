import Container from '@components/Container';
import { E84Logo } from './../../utils/constants';
import styles from './Footer.module.scss';

const Footer = ({ ...rest }) => {
  return (
    <footer className={styles.footer} {...rest}>
      <Container className={`${styles.footerContainer} ${styles.footerLegal}`}>
        <p>
        powered by <a href="https://element84.com" target="_blank">{E84Logo}</a> &copy; {new Date().getFullYear()}
        </p>
      </Container>
    </footer>
  );
};

export default Footer;
