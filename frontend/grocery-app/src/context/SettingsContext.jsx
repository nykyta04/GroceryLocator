import React, { createContext, useState } from 'react';

export const SettingsContext = createContext(null);

export const SettingsContextProvider = (props) => {
    const [glutenFree, setGlutenFree] = useState(localStorage.getItem("glutenFree") == "true" ? true : false);
    const [dairyFree, setDairyFree] = useState(localStorage.getItem("dairyFree") == "true" ? true : false);
    const [vegan, setVegan] = useState(localStorage.getItem("vegan") == "true" ? true : false);

    const toggleGlutenFree = () => {
        localStorage.setItem("glutenFree", !glutenFree);
        setGlutenFree(!glutenFree);
    }

    const toggleDairyFree = () => {
        localStorage.setItem("dairyFree", !dairyFree);
        setDairyFree(!dairyFree);
    }

    const toggleVegan = () => {
        localStorage.setItem("vegan", !vegan);
        setVegan(!vegan);
    }

    const contextValue = { 
        glutenFree,
        dairyFree,
        vegan,
        toggleGlutenFree,
        toggleDairyFree, 
        toggleVegan
    };

    return (
        <SettingsContext.Provider value={contextValue}>
          {props.children}
        </SettingsContext.Provider>
      );
}