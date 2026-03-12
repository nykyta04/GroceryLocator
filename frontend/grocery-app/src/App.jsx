import { useState } from 'react'
import './styles/App.css'
import { Routes, Route } from 'react-router-dom'
import Search from './pages/Search'
import ViewList from './pages/ViewList'
import ViewTotal from './pages/ViewTotal'
import Stores from './pages/Stores'
import Navbar from './components/Navbar'
import {ListContextProvider} from './context/ListContext'
import { SettingsContextProvider } from './context/settingsContext'
import StoreBreakdown from './pages/StoreBreakdown';   


function App() {
  return (
    <div>
      <ListContextProvider>
        <SettingsContextProvider>
          <Navbar />
          <Routes>
            <Route path="/" element={<Search/>}></Route>
            <Route path="/list" element={<ViewList/>}></Route>
            <Route path="/total" element={<ViewTotal/>}></Route>
            <Route path="/stores" element={<Stores/>} />
             <Route path="/breakdown" element={<StoreBreakdown />} />
          </Routes>
        </SettingsContextProvider>
      </ListContextProvider>
    </div>
)
}

export default App
