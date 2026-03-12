import { useEffect, useState } from "react";
import { useZip } from "../context/ZipContext";
import storeIcon from "../assets/Stores.png";
import pinIcon from "../assets/pin.png";
import storePin from "../assets/storePin.png";
import clockIcon from "../assets/clock.png";

// API base url
const BASE_URL = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// ---------- Helper functions ---------- //

// Handles fetch requests and JSON parsing
async function getJSON(url) {
  const res = await fetch(url);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Request failed ${res.status}: ${text || res.statusText}`);
  }
  return res.json();
}

// Fetch the single closest store based on ZIP
async function fetchClosestStore(zip) {
  return getJSON(`${BASE_URL}/api/stores/nearest/?zip=${encodeURIComponent(zip)}`);
}

// Fetch all nearby stores within selected radius
async function fetchStoresByZip(zip, radiusMiles) {
  return getJSON(
    `${BASE_URL}/api/stores/nearby/?zip=${encodeURIComponent(zip)}&radius=${encodeURIComponent(radiusMiles)}`
  );
}


// ---------- Main component ---------- //

// Global ZIP from context + the local state for radius and store data
export default function Stores() {
  const { zip } = useZip();
  const [radius, setRadius] = useState(10);
  const [closest, setClosest] = useState(null);
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Load stores when ZIP or radius changes
  useEffect(() => {
    if (!zip || String(zip).length !== 5) return;

    let cancelled = false;
    async function load() {
      setLoading(true);
      setError("");
      // Fetch closest stoe and all stores
      try {
        const [closestData, listData] = await Promise.all([
          fetchClosestStore(zip),
          fetchStoresByZip(zip, radius),
        ]);
        // Fallback for data differences
        const c = closestData.closest ?? closestData.store ?? closestData;
        const s = listData.stores ?? listData;
        if (!cancelled) {
          setClosest(c || null);
          setStores(Array.isArray(s) ? s : []);
        }
      } catch (e) {
        if (!cancelled) setError(e.message || "Failed to load stores");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
  }, [zip, radius]);

  // Format distance
  const fmtDist = (x) => {
    const d = x?.distance_mi ?? x?.distance ?? null;
    return d != null ? Number(d).toFixed(1) : null;
  };


// ---------- JSX structure ---------- //
  return (
    <div className="stores-wrap">
      <header className="stores-head">
        <h2 className="stores-title">
          <img src={storeIcon} alt="" className="icon-title-small" />
          Stores Near You
        </h2>
        <p>Find the best grocery stores near ZIP <strong>{zip || "—"}</strong></p>
      </header>

      {!zip && (
        <div className="card warn">
          No ZIP saved. Enter your ZIP in the header to see nearby stores.
        </div>
      )}

      {zip && (
        <section className="stores-controls">
          <label>
            Radius:&nbsp;
            <select value={radius} onChange={(e) => setRadius(Number(e.target.value))}>
              <option value={5}>5 miles</option>
              <option value={10}>10 miles</option>
              <option value={20}>20 miles</option>
              <option value={50}>50 miles</option>
            </select>
          </label>
          <span className="radius-count">
            {stores.length} store{stores.length === 1 ? "" : "s"} within {radius} mi
          </span>
        </section>
      )}

      {loading && <div className="card info">Loading stores…</div>}
      {error && <div className="card error">Error: {error}</div>}

      {zip && closest && !loading && (
        <section className="closest card">
          <div className="closest-content">
            <div className="closest-left">
              <img src={storeIcon} alt="" className="icon-lg" />
              <div>
                <div className="closest-title">Closest Store</div>
                <div className="closest-name">{closest.name}</div>
                <div className="closest-sub">
                  <img src={pinIcon} alt="" className="icon-sm" />
                  <span>{closest.address}</span>
                </div>
                {(closest.hour_open || closest.hour_close) && (
                  <div className="closest-hours">
                    <img src={clockIcon} alt="" className="icon-sm mr4" />
                    {closest.hour_open ?? "—"} — {closest.hour_close ?? "—"}
                  </div>
                )}
              </div>
            </div>

            <div className="closest-distance-badge">
                {Number(closest.distance_mi).toFixed(1)}
                <span>mi away</span>
                </div>
          </div>
        </section>
      )}

      {zip && (
        <section>
          <h3>All Stores</h3>
          <div className="table">
            <div className="thead">
              <div>Store</div>
              <div>Address</div>
              <div>Distance</div>
              <div>Hours</div>
            </div>

            <div className="tbody">
              {stores.map((s) => (
                <div className="trow" key={s.id ?? `${s.name}-${s.address}`}>
                  <div className="cell name">{s.name}</div>
                  <div className="cell">{s.address}</div>
                  <div className="cell">
                    <img src={storePin} alt="" className="icon-sm mr4" />
                    {fmtDist(s) ? `${fmtDist(s)} mi` : "—"}
                  </div>
                  <div className="cell">
                    <img src={clockIcon} alt="" className="icon-sm mr4" />
                    {(s.hour_open || s.hour_close)
                      ? `${s.hour_open ?? "—"}–${s.hour_close ?? "—"}`
                      : "—"}
                  </div>
                </div>
              ))}

              {!loading && stores.length === 0 && (
                <div className="trow empty">No stores within {radius} mi.</div>
              )}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
