import React, { useEffect, useRef } from "react";

const GMap = (props) => {
  const googleMapRef = useRef(null);
  let googleMap = null;
  const zoom = 4;
  // list of icons
  const iconList = {
    icon1:
      "https://cdn1.iconfinder.com/data/icons/Map-Markers-Icons-Demo-PNG/256/Map-Marker-Flag--Right-Chartreuse.png",
    icon2:
      "https://cdn2.iconfinder.com/data/icons/IconsLandVistaMapMarkersIconsDemo/256/MapMarker_Marker_Outside_Chartreuse.png",
    icon3:
      "https://cdn1.iconfinder.com/data/icons/Map-Markers-Icons-Demo-PNG/256/Map-Marker-Ball-Right-Azure.png",
    icon4:
      "https://cdn1.iconfinder.com/data/icons/Map-Markers-Icons-Demo-PNG/256/Map-Marker-Marker-Outside-Pink.png",
  };

  useEffect(() => {
    console.log(props);
    googleMap = initGoogleMap();
    var bounds = new window.google.maps.LatLngBounds();
    let marker = null;

    if (!props) {
      marker = createMarker({
        longitude: 2.407155402,
        latitude: 48.7646675418,
        name: "titi",
        icon: iconList.icon1,
        zoom: zoom,
      });
      googleMap.setZoom(zoom);
    } else {
      marker = createMarker({
        longitude: parseFloat(props.props.longitude),
        latitude: parseFloat(props.props.latitude),
        icon: iconList.icon1,
        zoom: zoom,
      });
      googleMap.setZoom(zoom);
    }

    bounds.extend(marker.position);
    googleMap.fitBounds(bounds);
  }, []);

  // initialize the google map
  const initGoogleMap = () => {
    return new window.google.maps.Map(googleMapRef.current, {
      center: {
        lat: parseFloat(props.props.latitude),
        lng: parseFloat(props.props.longitude),
      },
      zoom: zoom,
    });
  };

  // create marker on google map
  const createMarker = (markerObj) =>
    new window.google.maps.Marker({
      position: { lat: markerObj.latitude, lng: markerObj.longitude },
      map: googleMap,
      icon: {
        url: markerObj.icon,
        // set marker width and height
        scaledSize: new window.google.maps.Size(50, 50),
      },
      zoom: zoom,
    });

  return (
    <div ref={googleMapRef} style={{ width: 600, height: 500 }} zoom={zoom} />
  );
};

export default GMap;
