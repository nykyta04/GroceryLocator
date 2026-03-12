import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import {BrowserRouter} from 'react-router-dom'
import { ZipProvider } from './context/ZipContext.jsx'

createRoot(document.getElementById('root')).render(
<StrictMode>
  <BrowserRouter>
    <ZipProvider>
    <App />
    </ZipProvider>
  </BrowserRouter>,
</StrictMode>
)
