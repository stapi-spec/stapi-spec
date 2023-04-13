import styles from './Sidebar.module.scss'
import { useAppContext } from 'src/context/appContext';
import Button from '@components/Button';
import {
  ArrowRightLine
} from '@vectopus/atlas-icons-react';

import { ALL_PROVIDERS as providers } from 'src/utils/constants';

export default function RefinePane() {
  const { 
    userParams,
    setUserParams,
    setOpenFilters,
    products,
  } = useAppContext();

  function providerSelectHandler(e) {
    setUserParams({
      ...userParams,
      provider: e.target.value,
      product: 'all'
    })
  }

  function productSelectHandler(e) {
    setUserParams({
      ...userParams,
      product: e.target.value
    })
  }

  function constraintsSelectHandler(key, e){
    setUserParams({
      ...userParams,
      constraints: {
        ...userParams.constraints,
        [key]: e.target.value
      }
    })
  }

  function isProviderSelected(provider) {
    return provider === userParams.provider;
  }

  function isProductSelected(product) {
    return product === userParams.product;
  }

  function isConstraintSelected(constraint, key) {
    return userParams.constraints && constraint === userParams.constraints[key];
  }

  function getProductOptions(products){
    return products && products.filter(product => product).map(({ title, id }) => {
      return (
        <option
          key={id}
          value={id}
          selected={isProductSelected(id)}
        >
          {title}
        </option>
      );
    });
  }

  function displayProducts() {
    return userParams.provider !== 'all' ?
      getProductOptions(products[userParams.provider])
      : getProductOptions(Object.values(products).flat())
  }

//   //object of reduced constraints per provider
//   function getConstraints(p){
//   }

//   function displayProviderConstraints(){
//     return userParams.provider !== 'all' ? (
//         Object.entries(getConstraints(userParams.provider) ?? {}).map(([label, value]) => {
//             return (
//                 <div>
//                     <span className={styles.constraintLabel}>{label}: </span>
//                     <select onChange={e => constraintsSelectHandler(label, e)}  className={styles.refineSelection}>
//                     <option
//                         value=''
//                         key='default'
//                         selected
//                         >
//                     </option>
//                     {value.map((v) => (
//                         <option
//                         value={v}
//                         key={v}
//                         selected={isConstraintSelected(v, label)}
//                         >
//                         {v}
//                         </option>
//                     ))}
//                     </select>
//                 </div>
//             )
//         })
//      ) : null;
//   }

  return (
    <div className={styles.filtersFlyout}>
        <div className={styles.filtersTopBar}>
        <h4>Refine</h4>
        <Button
            className={styles.closeButton}
            onClick={() => setOpenFilters(false)}
        >
            <ArrowRightLine size={12} />
        </Button>
        </div>
        <div className={styles.filtersBody}>
        <div>
            <span className={styles.refineLabel}>Providers: </span>
            <select onChange={providerSelectHandler}  className={styles.refineSelection}>
            <option
                value='all'
                key='all'
                selected
                >
                All
                </option>
            {providers.map((provider) => (
                <option
                value={provider.id}
                key={provider.id}
                selected={isProviderSelected(provider.id)}
                >
                {provider.name}
                </option>
            ))}
            </select>
        </div>
        <div>
            <div className={styles.refineLabel}>Products: </div>
            <select onChange={productSelectHandler} className={styles.refineSelection}>
                <option
                value='all'
                key='all'
                selected
                >
                All
                </option>
                {displayProducts()}
            </select>
        </div>
        {userParams.provider !== 'all' && <div>
            <div className={styles.refineLabel}>Constraints: </div>
            {/* {displayProviderConstraints()} */}
        </div>}
        </div>
    </div>
    );
}
