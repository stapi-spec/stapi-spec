import { useMap } from 'react-leaflet';
import { useEffect, useState } from 'react';
import { useAppContext } from 'src/context/appContext';

import styles from './Map.module.scss';


function getCoords(geojson){
    return [geojson.geometry.coordinates[1], geojson.geometry.coordinates[0]]
}

export default function Footprint() {
    const map = useMap();
    const [activeMarkerHover, setActiveMarkerHover] = useState(null);
    const [previousMarkerHover, setPreviousMarkerHover] = useState(null);
    const [activeMarkerClick, setActiveMarkerClick] = useState(null);
    const [previousMarkerClick, setPreviousMarkerClick] = useState(null);
    const { selectedOpportunity, hoveredOpportunity } = useAppContext();
    const footprintIcon = new L.divIcon({className: styles.footprintCircle});

    useEffect(() => {
        if (!activeMarkerClick && previousMarkerClick){
            map.removeLayer(previousMarkerClick);
            setPreviousMarkerClick(null);
        }
        if (!activeMarkerHover && previousMarkerHover){
            map.removeLayer(previousMarkerHover);
            setPreviousMarkerHover(null);
        }
        if (activeMarkerClick && previousMarkerClick && (activeMarkerClick !== previousMarkerClick)){
            map.removeLayer(previousMarkerClick);
            setPreviousMarkerClick(activeMarkerClick);
        }
        previousMarkerHover && map.removeLayer(previousMarkerHover);
        activeMarkerHover && map.addLayer(activeMarkerHover);
        activeMarkerClick && map.addLayer(activeMarkerClick) && map.flyTo(getCoords(selectedOpportunity), 9);
    },[activeMarkerHover, previousMarkerHover, activeMarkerClick, previousMarkerClick]);

    useEffect(() => {
        activeMarkerHover && setPreviousMarkerHover(activeMarkerHover);
        activeMarkerClick && setPreviousMarkerClick(activeMarkerClick);
        if (hoveredOpportunity){
            setActiveMarkerHover(new L.Marker(getCoords(hoveredOpportunity), {
                icon: footprintIcon
            }));
        }
        else {
            setActiveMarkerHover(null);
        }

        if(selectedOpportunity) {
            setActiveMarkerClick(new L.Marker(getCoords(selectedOpportunity), {
                icon: footprintIcon
            }));
            setActiveMarkerHover(null);
        }
        else {
            setActiveMarkerClick(null);
        }
    }, [hoveredOpportunity, selectedOpportunity]);

    return null;
}
