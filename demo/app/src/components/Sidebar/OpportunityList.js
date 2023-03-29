import styles from './Sidebar.module.scss'
import Opportunity from './Opportunity';
import { useAppContext } from 'src/context/appContext';

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
        {opportunities.map((opp, index) => {
            return <Opportunity 
                key={index}
                title={opp.features[0].properties.title}
                start={opp.features[0].properties.start_datetime}
                end={opp.features[0].properties.end_datetime}
                // onMouseEnter={(e) => {
                //     mouseInStyleChange(e);
                //     setHoveredOpportunity(index)}}
                // onMouseLeave={(e) => {
                //     mouseOutStyleChange(e);
                //     setHoveredOpportunity(null)}}
                // onClick={(e) => setSelectedOpportunity(index)}
            />
        })
        }
    </div>
  );
}
