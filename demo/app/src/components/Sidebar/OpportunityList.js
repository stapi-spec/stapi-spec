import styles from './Sidebar.module.scss'
import Opportunity from './Opportunity';
import { useAppContext } from 'src/context/appContext';
import { parseStacDatetime } from 'src/utils';

export default function OpportunityList() {
  const { opportunities, setHoveredOpportunity, setSelectedOpportunity } = useAppContext();

  function mouseInStyleChange(e) {
    e.target.style.outline = 'red';
  }

function mouseOutStyleChange(e) {
  e.target.style.outline = 'none';
}

  return (
    <div className={styles.opportunityList}>
        {Object.entries(opportunities||{}).map(([provider, opps]) => {
            return opps && opps.map((opp, index) => {
              const { start, end } = parseStacDatetime(opp.properties.datetime);
              return <Opportunity
                  key={index}
                  title={opp.id}
                  provider={provider}
                  start={start}
                  end={end}
                  // onMouseEnter={(e) => {
                  //     mouseInStyleChange(e);
                  //     setHoveredOpportunity(index)}}
                  // onMouseLeave={(e) => {
                  //     mouseOutStyleChange(e);
                  //     setHoveredOpportunity(null)}}
                  // onClick={(e) => setSelectedOpportunity(index)}
              />
            })
        })
        }
    </div>
  );
}
