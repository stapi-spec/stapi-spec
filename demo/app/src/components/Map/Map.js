import dynamic from 'next/dynamic';
import { useState } from 'react';
import { useAppContext } from 'src/context/appContext';

// react-leaflet-draw styles
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw/dist/leaflet.draw.css'

const DynamicMap = dynamic(() => import('./DynamicMap'), {
  ssr: false
});

const DynamicEditControl = dynamic(
  {
    loader: () => import('react-leaflet-draw').then((rld) => rld.EditControl),
    render: (props, DynamicEditControl) => {
      return <DynamicEditControl {...props}></DynamicEditControl>
    }
  },
  {
    ssr: false
  }
);

const tileLayers = [{
  name: 'default',
  url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  attribution: '&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors'
},{
  name: 'Stadia.AlidadeSmooth',
  url: 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png',
  attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
},{
  name: 'Esri.WorldImagery',
  url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
}];

function whichMap(mapName) {
  return tileLayers.find(({ name }) => name === mapName);
}

const Map = (props) => {
  const [featureGroup, setFeatureGroup] = useState();
  const { userParams, setUserParams } = useAppContext();
  const { url, attribution } = whichMap('Stadia.AlidadeSmooth');

  /**
   * saves feature group ref for later editing
   */
  function onFeatureGroupReady(featureGroupRef) {
    setFeatureGroup(featureGroupRef);
  }

  /**
   * on layer created handler
   */
  function onCreated(e) {
    setUserParams({...userParams, bbox: e.layer.getBounds()});
  }

  /**
   * start drawing handler, deletes existing drawn layers
   */
  function onDrawStart() {
    const drawnItems = featureGroup._layers;
    const drawnItemKeys = Object.keys(drawnItems)
    drawnItemKeys.forEach((layerId, index) => {
      const layer = drawnItems[layerId];
      featureGroup.removeLayer(layer);
    });
  }

  return (
    <div style={{ height: '100%', height: '100%' }}>
      <DynamicMap {...props}>
        {(module) => {
        const { FeatureGroup, TileLayer } = module;
          return (
            <>
              <TileLayer
                url={url}
                attribution={attribution}
              />
              <FeatureGroup
                ref={(featureGroupRef) => {
                  onFeatureGroupReady(featureGroupRef);
                }}
              >
                <DynamicEditControl
                  position="topleft"
                  draw={{
                    circle: false,
                    circlemarker: false,
                    marker: false,
                    polygon: true,
                    polyline: false,
                    rectangle: false,
                  }}
                  onCreated={onCreated}
                  onDrawStart={onDrawStart}
                />
                {props.children}
              </FeatureGroup>
            </>
          )}}
      </DynamicMap>
    </div>
  )
}

export default Map;
