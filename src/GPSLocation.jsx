import React, { useEffect, useRef, useState } from 'react';
import { MapPin, Navigation, LocateFixed, Square, ExternalLink, WifiOff, ShieldCheck, AlertTriangle } from 'lucide-react';
import { db } from './offline/database';
import { PageTitle, Panel } from './components';

function formatCoords(p) {
  return `${p.latitude.toFixed(6)}, ${p.longitude.toFixed(6)}`;
}

export default function GPSLocation() {
  const [position, setPosition] = useState(null);
  const [savedPosition, setSavedPosition] = useState(null);
  const [tracking, setTracking] = useState(false);
  const [message, setMessage] = useState('GPS is off. Press “Get my location” and allow browser location access.');
  const [error, setError] = useState('');
  const watchId = useRef(null);

  useEffect(() => {
    db.meta.get('last-location').then((record) => {
      if (record?.value) {
        setSavedPosition(record.value);
        setPosition(record.value);
        setMessage('Showing your last location saved on this device. It may be outdated.');
      }
    }).catch(() => {});
    return () => {
      if (watchId.current !== null && navigator.geolocation) navigator.geolocation.clearWatch(watchId.current);
    };
  }, []);

  async function storePosition(p) {
    const record = {
      latitude: p.coords.latitude,
      longitude: p.coords.longitude,
      accuracy: p.coords.accuracy,
      timestamp: new Date(p.timestamp).toISOString(),
    };
    setPosition(record);
    setSavedPosition(record);
    await db.meta.put({ key: 'last-location', value: record });
    setError('');
    setMessage(`Location updated at ${new Date(record.timestamp).toLocaleTimeString()}. Coordinates are saved locally on this device.`);
  }

  function handlePositionError(e) {
    setError(e.code === 1 ? 'Location permission was denied. Allow location access in your browser settings and try again.' : e.code === 2 ? 'Your device could not determine a location. Check device location services and try again.' : 'Location request timed out. Move to an area with a clearer GPS signal and retry.');
    setTracking(false);
    if (watchId.current !== null && navigator.geolocation) navigator.geolocation.clearWatch(watchId.current);
    watchId.current = null;
  }

  function getLocation() {
    setError('');
    if (!navigator.geolocation) {
      setError('This browser does not support geolocation. Try a recent browser on localhost or HTTPS.');
      return;
    }
    setMessage('Requesting your location permission…');
    navigator.geolocation.getCurrentPosition(async (p) => {
      try { await storePosition(p); } catch { setError('Location was received, but could not be saved locally.'); }
    }, handlePositionError, { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 });
  }

  function startTracking() {
    if (!navigator.geolocation) {
      setError('This browser does not support geolocation.');
      return;
    }
    if (watchId.current !== null) return;
    setError('');
    setTracking(true);
    setMessage('Live location updates are active while this page remains open.');
    watchId.current = navigator.geolocation.watchPosition(async (p) => {
      try { await storePosition(p); } catch { setError('Could not save the latest location locally.'); }
    }, handlePositionError, { enableHighAccuracy: true, timeout: 20000, maximumAge: 3000 });
  }

  function stopTracking() {
    if (watchId.current !== null && navigator.geolocation) navigator.geolocation.clearWatch(watchId.current);
    watchId.current = null;
    setTracking(false);
    setMessage('Live updates stopped. Your last saved coordinates remain on this device.');
  }

  async function clearSavedLocation() {
    stopTracking();
    await db.meta.delete('last-location');
    setPosition(null);
    setSavedPosition(null);
    setMessage('Saved location removed from this device.');
    setError('');
  }

  const p = position || savedPosition;
  const mapUrl = p ? `https://www.openstreetmap.org/export/embed.html?bbox=${p.longitude - 0.008}%2C${p.latitude - 0.005}%2C${p.longitude + 0.008}%2C${p.latitude + 0.005}&layer=mapnik&marker=${p.latitude}%2C${p.longitude}` : null;
  const externalMap = p ? `https://www.google.com/maps?q=${p.latitude},${p.longitude}` : null;

  return <>
    <PageTitle eyebrow="GPS LOCATION" title="Your location, on your terms." description="Use your device's location permission to get coordinates, view them on a map, and optionally watch updates while this page is open." action={<span className={'connection ' + (tracking ? 'online' : 'offline')}>{tracking ? <Navigation size={15}/> : <MapPin size={15}/>} {tracking ? 'Live updates on' : 'Tracking off'}</span>} />
    <div className="content-grid gps-grid">
      <Panel title="Location controls" subtitle="Location is requested only when you choose it">
        <div className="gps-actions">
          <button className="btn" onClick={getLocation}><LocateFixed size={16}/> Get my location</button>
          {!tracking ? <button className="secondary-btn" onClick={startTracking}><Navigation size={15}/> Start live updates</button> : <button className="secondary-btn" onClick={stopTracking}><Square size={15}/> Stop live updates</button>}
        </div>
        {error && <div className="error-msg gps-message"><AlertTriangle size={15}/>{error}</div>}
        <div className="status-message gps-message"><ShieldCheck size={16}/>{message}</div>
        {p ? <div className="gps-details">
          <div><small>LATITUDE / LONGITUDE</small><b>{formatCoords(p)}</b></div>
          <div><small>ACCURACY</small><b>{Number.isFinite(p.accuracy) ? `±${Math.round(p.accuracy)} metres` : 'Not available'}</b></div>
          <div><small>LOCATION TIMESTAMP</small><b>{new Date(p.timestamp).toLocaleString()}</b></div>
          <div className="gps-actions"><a className="btn" href={externalMap} target="_blank" rel="noreferrer">Open in Google Maps <ExternalLink size={14}/></a><button className="secondary-btn" onClick={clearSavedLocation}>Clear saved location</button></div>
        </div> : <div className="gps-empty"><MapPin size={26}/><b>No location captured yet</b><span>Allow location access to see your coordinates and map.</span></div>}
        <p className="gps-disclaimer"><WifiOff size={14}/> The last saved coordinates can be viewed offline, but online map tiles need internet. Live updates may stop when this tab is suspended or closed. This page does not silently share your location with contacts or the server.</p>
      </Panel>
      <Panel title="Location map" subtitle={p ? 'Map marker uses your most recently saved coordinates' : 'Capture a location to place a map marker'}>
        {p && mapUrl ? <div className="gps-map-wrap"><iframe title="Map showing your last saved location" src={mapUrl} loading="lazy" referrerPolicy="no-referrer"/><span className="map-caption">Map tiles are provided by OpenStreetMap and require an internet connection.</span></div> : <div className="gps-empty gps-map-empty"><MapPin size={32}/><b>Your map will appear here</b><span>Press “Get my location” to place a marker.</span></div>}
      </Panel>
    </div>
    <div className="notice"><ShieldCheck size={18}/><div><b>Privacy and safety note</b><p>Browser GPS needs permission and typically requires HTTPS or localhost. Location accuracy depends on your device. This feature records coordinates on this device only; emergency contact sharing and background tracking are not enabled by it.</p></div></div>
  </>;
}
