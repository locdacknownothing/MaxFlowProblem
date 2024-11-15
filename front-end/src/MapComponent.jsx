import React, { useState, useRef, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "leaflet-routing-machine";
import dataPoints from "./data/full_node_data.json";
import dataEdges from "./data/full_edge_data.json";

const customIcon = new L.Icon({
  iconUrl: "pin.png",
  iconSize: [32, 35],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const startIcon = new L.Icon({
  iconUrl: "start_icon.png",
  iconSize: [16, 16],
  iconAnchor: [16, 16],
  popupAnchor: [0, 0],
});

const endIcon = new L.Icon({
  iconUrl: "end_icon.png",
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
  const [selectedPoints, setSelectedPoints] = useState([]);
  const mapRef = useRef(null);
  const routingControlRef = useRef(null);

  const handlePointClick = (point) => {
    if (selectedPoints.length >= 2) return;
    setSelectedPoints((prevPoints) => [...prevPoints, point]);
  };

  useEffect(() => {
    if (!mapRef.current || selectedPoints.length < 2) return;

    if (routingControlRef.current) {
      routingControlRef.current.remove();
      routingControlRef.current = null;
    }

    routingControlRef.current = L.Routing.control({
      waypoints: selectedPoints.map((point) => L.latLng(point.lat, point.lon)),
      lineOptions: {
        styles: [{ color: "#024EC0", opacity: 0.8, weight: 4 }],
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
        style={{ height: "700px", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
        />
        <MapWrapper mapRef={mapRef} />
        {dataEdges.map((edge, index) => (
         <Polyline key={index} positions={[[dataPoints[edge.src].lat, dataPoints[edge.src].lon], [dataPoints[edge.dst].lat, dataPoints[edge.dst].lon]]} color="blue" />
        ))}
        {dataPoints.map((point) => (
          <Marker
            key={point.id}
            position={[point.lat, point.lon]}
            icon={customIcon}
            eventHandlers={{
              click: () => handlePointClick(point),
            }}
          >
            <Popup>{point.index}</Popup>
          </Marker>
        ))}
      </MapContainer>
      {selectedPoints.length === 2 && (
        <button onClick={handleReset} style={{ marginTop: "10px" }}>
          Chọn lại điểm
        </button>
      )}
    </div>
  );
};

export default MapComponent;