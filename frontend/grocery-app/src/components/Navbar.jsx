import { useState, useEffect, useContext } from 'react'
import React from 'react'; 
import {Link} from 'react-router-dom'
import '../styles/App.css'
import listIcon from '../assets/listview.png'
import searchIcon from '../assets/search.png'
import pinIcon from '../assets/pin.png'
import storesIcon from '../assets/Stores.png'
import { useZip } from '../context/ZipContext'
import { SettingsContext } from '../context/settingsContext';


const Navbar = () => {
  const { zip, error, saveZip, clearZip } = useZip()
  const [draft, setDraft] = useState("")
  const [settingsToggled, setSettingsToggled] = useState(false);
  const {toggleGlutenFree, toggleDairyFree, toggleVegan, glutenFree, dairyFree, vegan} = useContext(SettingsContext);

  useEffect(() => {
    if (!zip) setDraft("");
  }, [zip]);

  const handleSave = () => {
    const ok = saveZip(draft)
    if (ok) setDraft("")
  };


  return (
    <div className='navbar-and-settings'>
      <div className='navbar'>
        {/*Settings button*/}
        <button className="settings-btn" onClick={() => setSettingsToggled(!settingsToggled)}>Dietary Filters</button>

        {/* ZIP controls */}
        <div className="zip-section">
          {/* Show badge ONLY when a ZIP is saved */}
          {zip && (
            <span className="zip-badge">
              <img src={pinIcon} alt="location" className="pin-img" />
              <span className="zip-text">{zip}</span>
              <button className="chip-clear" onClick={clearZip} title="Clear ZIP">×</button>
            </span>
          )}

          <input
            type="text"
            placeholder="Enter ZIP"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            maxLength={5}
            inputMode="numeric"
            className="zip-input pretty"
          />
          <button className="btn-primary" onClick={handleSave}>Save</button>
          {error && <div className="zip-error">{error}</div>}
        </div>
      
        <ul>
          <div className='navbar-link'><Link to="/"><li><img src={searchIcon}></img>Search</li></Link></div>
          <div className='navbar-link'><Link to="/list"><li><img src={listIcon}></img>View List</li></Link></div>
          <div className='navbar-link'><Link to="/stores"><li><img src={storesIcon} alt="stores icon" />Stores</li></Link></div>
        </ul>
      </div>
      {settingsToggled ? (<div className="settings-menu">
        <label for="gluten-free" className='settings-checkbox-label'>
          <input onChange={() => toggleGlutenFree()} className='settings-checkbox' type="checkbox" id="gluten-free" name="gluten-free" value="gluten-free" checked={glutenFree}/>
          Gluten-Free
        </label><br></br>

        <label for="dairy-free" className='settings-checkbox-label'>
          <input onChange={() => toggleDairyFree()} className='settings-checkbox' type="checkbox" id="dairy-free" name="dairy-free" value="dairy-free" checked={dairyFree}/>
          Dairy-Free
        </label><br></br>

        <label for="vegan" className='settings-checkbox-label'>
          <input onChange={() => toggleVegan()} className='settings-checkbox' type="checkbox" id="vegan" name="vegan" value="vegan" checked={vegan}/>
          Vegan
        </label><br></br>
      </div>) : (<></>)}
      
    </div>
  
  );
};

export default Navbar