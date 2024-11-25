import React, { useState, useRef, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
  Polyline,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "leaflet-routing-machine";
import dataPoints from "./data/manual_node_data.json";
import dataEdges from "./data/manual_edge_data.json";
import axios from "axios";

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

const algorithms = {
  mpm: "Ford Fulkerson",
  edmonds_karp: "Edmonds Karp",
  capacity_scaling: "Capacity Scaling",
  fifo_push_relabel: "FIFO Push Relabel",
};

const MapComponent = () => {
  const [selectedPoints, setSelectedPoints] = useState([]);
  const mapRef = useRef(null);
  const routingControlRef = useRef(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("");
  const [edges, setEdges] = useState(dataEdges);

  const handlePointClick = (point) => {
    if (selectedPoints.length >= 2) return;
    setSelectedPoints((prevPoints) => [...prevPoints, point]);
  };

  // useEffect(async () => {
  //   if (!mapRef.current || selectedPoints.length < 2) return;

  //   if (routingControlRef.current) {
  //     routingControlRef.current.remove();
  //     routingControlRef.current = null;
  //   }

  //   // const response = await axios.post(
  //   //   `http://localhost:3000/${selectedAlgorithm}`,
  //   //   {
  //   //     source: parseInt(selectedPoints[0].node_id),
  //   //     sink: parseInt(selectedPoints[1].node_id),
  //   //   }
  //   // );

  //   // console.log(response.data);

  //   routingControlRef.current = L.Routing.control({
  //     waypoints: selectedPoints.map((point) => L.latLng(point.lat, point.lon)),
  //     lineOptions: {
  //       styles: [{ color: "#024EC0", opacity: 0.8, weight: 4 }],
  //     },
  //     createMarker: (i, waypoint, n) => {
  //       const icon = i === 0 ? startIcon : i === n - 1 ? endIcon : startIcon;
  //       return L.marker(waypoint.latLng, { icon });
  //     },
  //     show: false,
  //   }).addTo(mapRef.current);
  // }, [selectedPoints]);

  useEffect(() => {
    const updateRoutingControl = async () => {
      const map = mapRef.current;
      if (!map || selectedPoints.length < 2) return;

      // Remove existing routing control if it exists
      if (routingControlRef.current) {
        map.removeControl(routingControlRef.current);
        routingControlRef.current = null;
      }
      console.log(selectedPoints);

      try {
        // Call the API
        const response = await axios.post(
          `http://localhost:3000/${selectedAlgorithm}`,
          {
            source: parseInt(selectedPoints[0].index),
            sink: parseInt(selectedPoints[1].index),
          }
        );

        setEdges(response.data.edges);

        // Process API response if needed
        const { edges } = response.data;

        // Optionally, create new routing control based on API response
        routingControlRef.current = L.Routing.control({
          waypoints: edges.map((edge) => L.latLng(edge.lat, edge.lon)), // Adjust according to API response format
          lineOptions: {
            styles: [{ color: "#024EC0", opacity: 0.8, weight: 4 }],
          },
          createMarker: (i, waypoint, n) => {
            const icon =
              i === 0 ? startIcon : i === n - 1 ? endIcon : startIcon;
            return L.marker(waypoint.latLng, { icon });
          },
          show: false,
        }).addTo(map);
      } catch (error) {
        console.error("Error fetching data from API:", error);
      }
    };

    updateRoutingControl();
  }, [selectedPoints, selectedAlgorithm]);

  const handleReset = () => {
    setSelectedPoints([]);
    const map = mapRef.current;
    if (routingControlRef.current) {
      map.removeControl(routingControlRef.current);
      routingControlRef.current = null;
    }
  };

  const handleSelect = async (key) => {
    setSelectedAlgorithm(key);
    console.log(`Selected: ${algorithms[key]}`);
  };

  return (
    <div>
      <div className="container mt-2">
        <div className="dropdown">
          <button
            className="btn btn-primary dropdown-toggle"
            type="button"
            id="dropdownMenuButton"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            {selectedAlgorithm
              ? algorithms[selectedAlgorithm]
              : "Select Algorithm"}
          </button>
          <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton">
            {Object.entries(algorithms).map(([key, value]) => (
              <li key={key}>
                <button
                  className="dropdown-item"
                  onClick={() => handleSelect(key)}
                >
                  {value}
                </button>
              </li>
            ))}
          </ul>
        </div>
        {selectedAlgorithm && (
          <div className="mt-2">
            <p>
              <strong>Selected Algorithm:</strong>{" "}
              {algorithms[selectedAlgorithm]}
            </p>
          </div>
        )}
      </div>
      {selectedPoints.length === 2 && (
        <button
          className="btn btn-primary"
          onClick={handleReset}
          style={{ marginTop: "10px" }}
        >
          Chọn lại điểm
        </button>
      )}
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
        {/* {!!dataEdges &&
          dataEdges.map((edge, index) => (
            <Polyline
              key={index}
              positions={[
                [dataPoints[edge.src].lat, dataPoints[edge.src].lon],
                [dataPoints[edge.dst].lat, dataPoints[edge.dst].lon],
              ]}
              color="blue"
            />
          ))} */}
        {edges &&
          edges.map((edge, index) => {
            const srcPoint = dataPoints[edge.src];
            const dstPoint = dataPoints[edge.dst];
            const centerLat = (srcPoint.lat + dstPoint.lat) / 2;
            const centerLon = (srcPoint.lon + dstPoint.lon) / 2;
            let color = "blue";
            if (typeof edge.capacity !== "number") {
              const [endWeight, startWeight] = edge.capacity
                .split("/")
                .map(Number);
              color = startWeight === endWeight ? "blue" : "red";
            }
            const weight = edge.capacity;

            return (
              <React.Fragment key={index}>
                <Polyline
                  positions={[
                    [srcPoint.lat, srcPoint.lon],
                    [dstPoint.lat, dstPoint.lon],
                  ]}
                  color={color}
                />

                <Marker
                  position={[centerLat, centerLon]}
                  icon={L.divIcon({
                    className: "text-marker", // Custom class for styling
                    html: `<div style="background-color: white; padding: 2px 4px; border-radius: 4px; font-size: 12px; border: 1px solid black; display: inline-block;">${weight}</div>`,
                  })}
                  interactive={false} // Disable interaction for this marker
                />
              </React.Fragment>
            );
          })}
        {!!dataPoints &&
          dataPoints.map((point) => (
            <Marker
              key={point.id}
              position={[point.lat, point.lon]}
              icon={customIcon}
              eventHandlers={{
                click: () => handlePointClick(point),
              }}
            >
              <Popup>{`${point.index}`}</Popup>
            </Marker>
          ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
