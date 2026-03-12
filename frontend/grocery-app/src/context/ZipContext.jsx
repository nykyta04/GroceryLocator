import { createContext, useContext, useEffect, useState } from "react";

const ZipCtx = createContext(null);
export const useZip = () => useContext(ZipCtx);

//  5-digit validator
export const isValidZip = (z) => /^\d{5}$/.test(String(z || "").trim());

export function ZipProvider({ children }) {
  const [zip, setZip] = useState(() => localStorage.getItem("zip") || "");
  const [error, setError] = useState("");

  // Check valid format (5 digits)
  const saveZip = (z) => {
    const cleaned = String(z || "").trim();
    if (!isValidZip(cleaned)) {
      setError("Enter a valid 5-digit ZIP");
      return false;
    }

    if (cleaned === "00000") {
      setError('"00000" is not a valid ZIP code');
      return false;
    }

    setError("");
    setZip(cleaned);
    localStorage.setItem("zip", cleaned);
    return true;
  };

  const clearZip = () => {
    localStorage.removeItem("zip");
    setZip("");
    setError("");
  };

  // keep zipcode state in sync if another tab changes it
  useEffect(() => {
    const onStorage = (e) => {
      if (e.key === "zip") setZip(e.newValue || "");
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  return (
    <ZipCtx.Provider value={{ zip, error, saveZip, clearZip }}>
      {children}
    </ZipCtx.Provider>
  );
}
