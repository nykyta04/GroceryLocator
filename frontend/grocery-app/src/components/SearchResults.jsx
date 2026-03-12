import React from 'react';
import { useContext, useEffect, useMemo, useState } from "react";
import { ITEMS } from '../items';
import { ListContext } from "../context/ListContext";
import { SettingsContext } from '../context/settingsContext';

//  Base API URL
const BASE_URL = import.meta.env.VITE_API_URL

// ------------SearchResults Component-----------
export default function SearchResults({ query }) {
  const { addToList } = useContext(ListContext);
  const {glutenFree, dairyFree, vegan} = useContext(SettingsContext);
  const [apiHits, setApiHits] = useState([]);
  const q = (query || "").trim().toLowerCase();


  // Fetch matching grocery items from backend(debounced)
  useEffect(() => {
    let t;
    // If query is empty, clear results
    if (!q) { setApiHits([]); return; }

    // Debouced fetch to avoid spamming requests while typing
    t = setTimeout(async () => {
      // Fetch from Django API search endpoint
      try {
        const r = await fetch(
          `${BASE_URL}grocery-items/search/?q=${encodeURIComponent(q)}`
        );
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        // Parse and validate response
        const data = await r.json();
        setApiHits(Array.isArray(data) ? data : []);
      } catch (e) {
        console.error("search error:", e);
        setApiHits([]); // fallback to empty results if errors
      }
    }, 200); // debounce set to 200ms to avoid spamming too many requests
    return () => clearTimeout(t);
  }, [q]);


  // Merge: local base items + API hits (brand or item)
  const rows = useMemo(() => {
    // With an empty query, just show the base items 
    if (!q) {
      return ITEMS.filter((i) => 
        //Gluten-free filter
        (glutenFree && i.tags.includes("gluten-free")) || !glutenFree
      ).filter((i) => 
        //Dairy-free filter
        (dairyFree && i.tags.includes("dairy-free")) || !dairyFree
      ).filter((i) => 
        //Vegan filter
        (vegan && i.tags.includes("vegan")) || !vegan
      ).map(i => ({
        kind: "base",         // identifies local base item
        label: i.itemName,    // what we display in the list
        addId: i.id,          // the id we add to the list
        key: `base:${i.id}`,  // React rendering
      }));
    }


    // Local base items matching the query
    const base = ITEMS
      .filter((i) => 
        //Gluten-free filter
        (glutenFree && i.tags.includes("gluten-free")) || !glutenFree
      ).filter((i) => 
        //Dairy-free filter
        (dairyFree && i.tags.includes("dairy-free")) || !dairyFree
      ).filter((i) => 
        //Vegan filter
        (vegan && i.tags.includes("vegan")) || !vegan
      )
      .filter(i => i.itemName.toLowerCase().includes(q))
      .map(i => ({
        kind: "base",
        label: i.itemName,
        addId: i.id,
        key: `base:${i.id}`,
      }));

      
    // Map backend (either brand or item)
    const api = apiHits.map(h => ({
      kind: h.brand?.toLowerCase().includes(q) ? "brand" : "item",
      label: h.name,          // display item name
      brand: h.brand,         // display brand (if any)
      itemName: h.item_name,  // base item from database for mapping
      key: `api:${h.id}`,
    }));

    // Merge both results in search
    return [...base, ...api];
  }, [q, apiHits]);


  // Helper function: Map a brand hit back to the base item id
  const addByItemName = (itemName) => {
    const id = ITEMS.find(
      x => x.itemName.toLowerCase() === (itemName || "").toLowerCase()
    )?.id;
    // Keep storing list entries as base item IDs
    if (id !== undefined) addToList(id); // keep existing list format (ids)
  };


  // Render the search results (+ jsx)
  return (
    <div className="search-item-container">
      {rows.map(r => (
        <div className="search-item" key={r.key}>
          <p>
            {r.label} {r.brand ? <em>— {r.brand}</em> : null}
          </p>
          <button
            onClick={() =>
              r.kind === "base" ? addToList(r.addId) : addByItemName(r.itemName)
            }
          >
            +
          </button>
        </div>
      ))}
    </div>
  );
};

