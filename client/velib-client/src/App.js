import React   from 'react';
import {useState} from 'react';
 

const App = () => {
  const [longitude, setLongitude] = useState(0);
  const [latitude, setLatitude] = useState(0);
  const [foundVelib, setFoundVelib] = useState({});
 ;
  const handleChangeLongitude = event => {
    setLongitude(event.target.value);
  };
  const handleChangeLatitude = event => {
  setLatitude(event.target.value);
  };

  const defaultProps = {
    center: {
      lat: 10.99835602,
      lng: 77.01502627
    },
    zoom: 11
  };

function findVelib(){
  fetch( `http://localhost:9090/find/velib?longitude=${longitude}&latitude=${latitude}`, {
    headers: new Headers({
      'Authorization': 'Basic '+btoa('toto:titi'), 
      
  })
  } )
  .then(res => res.json())
  .then(
    (result) => {
      setFoundVelib(result);
      
    },
    (error) => {
     console.log(error)
    }
  )
}

  return (
    <div>
  <label>
    Longitude :
    <input
        type="text"
        id="longitude"
        name="longitude"
        onChange={handleChangeLongitude}
        value={longitude}
      />
  </label>
  

  <label>
    Latitude :
   <input
        type="text"
        id="latitude"
        name="latitude"
      
        onChange={handleChangeLatitude}
        value={latitude}
      />
  </label>
  
  <button onClick={findVelib}>
  Find Velib
</button>

    Station = { foundVelib.name}


    </div>
  );
};

export default App;