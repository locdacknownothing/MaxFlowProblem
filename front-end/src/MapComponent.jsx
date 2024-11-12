import React, { useState, useRef, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import 'leaflet-routing-machine';
import dataPoints from './data/node_data2.json';
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

const MapComponent = () => {
  // const [dataPoints, setDataPoints] = useState([]); // State to store points from data.json
  const [selectedPoints, setSelectedPoints] = useState([]); 
  const mapRef = useRef(null); 
  const routingControlRef = useRef(null); 

  // Load data from data.json on component mount
  // useEffect(() => {
  //   fetch('C:/Users/gguu/Project/MaxFlowProblem/data/results/node_data3.json')
  //     .then((response) => response.json())
  //     .then((data) => {
  //       const formattedPoints = data.map((point) => ({
  //         id: point.node_id,
  //         lat: point.lat,
  //         lng: point.lon,
  //       }));
  //       setDataPoints(formattedPoints);
  //     })
  //     .catch((error) => console.error('Error loading data:', error));
  // }, []);

  const handlePointClick = (point) => {
    if (selectedPoints.length >= 2) return; 
    setSelectedPoints((prevPoints) => [...prevPoints, point]); 
  };

  useEffect(() => {
    if (!mapRef.current || selectedPoints.length < 2) return;

    if (routingControlRef.current) {
      routingControlRef.current.remove();
    }

    const listPoints = [
      {lat: 10.775593970389078, lng: 106.68259406549535},
      {lat: 10.777633749235925, lng: 106.68238189411164},
      {lat: 10.786236010591294, lng: 106.69771786704939},
    ];

    routingControlRef.current = L.Routing.control({
      waypoints: listPoints.map((point) => L.latLng(point.lat, point.lng)),
      lineOptions: {
        styles: [{ color: '#024EC0', opacity: 0.8, weight: 4 }],
      },
      createMarker: (i, waypoint, n) => {
        const icon = i === 0 ? startIcon : i === n - 1 ? endIcon : startIcon;
        return L.marker(waypoint.latLng, { icon });
      },
      show: false,
    }).addTo(mapRef.current);
  }, [selectedPoints]);

  const handleReset = () => {
    setSelectedPoints([]);
    if (routingControlRef.current) {
      routingControlRef.current.getPlan().setWaypoints([]);
    }
  };

  return (
    <div>
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
            icon={customIcon}
            eventHandlers={{
              click: () => handlePointClick(point),
            }}
          >
            <Popup>{point.display_name}</Popup>
          </Marker>
        ))}
      </MapContainer>
      {selectedPoints.length === 2 && (
        <button onClick={handleReset} style={{ marginTop: '10px' }}>
          Chọn lại điểm
        </button>
      )}
    </div>
  );
};

export default MapComponent;