import React, { useEffect } from "react";
import { useState } from "react";
import GMap from "./gmap";
import Card from 'react-bootstrap/Card';
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';

require('dotenv').config()



const App = () => {
  const API_KEY = process.env.GOOGLE_MAP_API_KEY;
  const [, updateState] = React.useState();
  const [longitude, setLongitude] = useState(0);
  const [latitude, setLatitude] = useState(0);
  const [foundVelib, setFoundVelib] = useState({});
  const handleChangeLongitude = (event) => {
    setLongitude(event.target.value);
  };
  const handleChangeLatitude = (event) => {
    setLatitude(event.target.value);
  };

 
  const [loadMap, setLoadMap] = useState(false);

  useEffect(() => {
    loadGoogleMapScript(() => {
      setLoadMap(false);
    });
  }, []);
  // load google map script
  const loadGoogleMapScript = (callback) => {
    if (
      typeof window.google === "object" &&
      typeof window.google.maps === "object"
    ) {
      callback();
    } else {
      console.log(process.env);
      const googleMapScript = document.createElement("script");
      googleMapScript.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}`;
      window.document.body.appendChild(googleMapScript);
      googleMapScript.addEventListener("load", callback);
    }
  };
  const forceUpdate = React.useCallback(() => updateState({}), []);

  function findVelib() {
    fetch(
      `/find/velib?longitude=${longitude}&latitude=${latitude}`,
      {
        headers: new Headers({
          Authorization: "Basic " + btoa("toto:titi"),
        }),
      }
    )
      .then((res) => res.json())
      .then(
        (result) => {
          forceUpdate();
          setLoadMap(false);
          setFoundVelib(result);
          console.log("server response ", result);
          setLoadMap(true);
        },
        (error) => {
          console.log(error);
        }
      );
  }

  return (   
    <>
    <Card>
      <Card.Header>Trouver un velib </Card.Header>
      <Card.Body>
      <input
          type="number"
          id="longitude"
          name="longitude"
          onChange={handleChangeLongitude}
          value={longitude}
        />
        <input
          type="number"
          id="latitude"
          name="latitude"
          onChange={handleChangeLatitude}
          value={latitude}
        />
       
       <Button variant="primary" type="submit" onClick={findVelib}>
      Find Velib
      </Button>
      </Card.Body>
    </Card>
      Station = {foundVelib.name}
      {!loadMap ? <div>Loading...</div> : <GMap props={foundVelib} />}
    </>

  );
};

export default App;
