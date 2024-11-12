import React, { useState, useRef, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import 'leaflet-routing-machine';
import dataPoints from './data/node_data3.json';

const customIcon = new L.Icon({
  iconUrl: 'pin.png',
  iconSize: [32, 35],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const startIcon = new L.Icon({
  iconUrl: 'start_icon.png',
  iconSize: [16, 16],
  iconAnchor: [16, 16],
  popupAnchor: [0, 0],
});

const endIcon = new L.Icon({
  iconUrl: 'end_icon.png',
  iconSize: [32, 35],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const MapWrapper = ({ mapRef }) => {
  const map = useMap();
  useEffect(() => {
    mapRef.current = map;
  }, [map, mapRef]);
  return null;
};

const TempComponent = () => {
  const [selectedPoints, setSelectedPoints] = useState([]);
  const [selectedPointIds, setSelectedPointIds] = useState({});
  const mapRef = useRef(null);

  const handlePointClick = (point) => {
    if (selectedPointIds[point.node_id]) return; // Skip if the point is already selected

    setSelectedPoints((prevPoints) => [...prevPoints, point]);
    setSelectedPointIds((prevIds) => ({ ...prevIds, [point.node_id]: true }));
  };

  const handleReset = () => {
    setSelectedPoints([]);
    setSelectedPointIds({});
  };

  const handleExport = () => {
    const data = JSON.stringify(selectedPoints, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'selected_points.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      {selectedPoints.length > 0 && (
        <div style={{ marginTop: '10px' }}>
          <button onClick={handleExport}>Export</button>
          <button onClick={handleReset} style={{ marginRight: '10px' }}>
              Reset
          </button>
        </div>
      )}
      <MapContainer
        center={[10.762622, 106.660172]}
        zoom={13}
        style={{ height: '700px', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
        />
        <MapWrapper mapRef={mapRef} />
        {dataPoints.map((point) => (
          <Marker
            key={point.id}
            position={[point.lat, point.lon]}
            icon={selectedPointIds[point.node_id] ? endIcon : customIcon}
            eventHandlers={{
              click: () => handlePointClick(point),
            }}
          >
            <Popup>{point.lat},{point.lon}</Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default TempComponent;