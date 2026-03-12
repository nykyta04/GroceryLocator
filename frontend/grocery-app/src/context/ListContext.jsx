import React, { createContext, useState } from 'react';

export const ListContext = createContext(null);

export const ListContextProvider = (props) => {
  const [listItems, setListItems] = useState({ items: [] });
  // simple feedback text 
  const [feedback, setFeedback] = useState("");

  const addToList = (itemId) => {
    setListItems((prev) => {
      // copy to avoid mutating states
      const newItems = [...prev.items];

      if (!newItems.includes(itemId)) {
        newItems.push(itemId);
        setFeedback("Item added to your list.");
      } else {
        setFeedback("Item is already in your list.");
      }
      return { items: newItems };
    });
  };
  
  const removeFromList = (itemId) => {
  setListItems((prev) => {
    const newItems = [...prev.items];          
    const idx = newItems.indexOf(itemId);
    if (idx !== -1) {
      newItems.splice(idx, 1);
    }
    return { items: newItems };
  });
};


  const contextValue = {
    listItems,
    addToList,
    removeFromList,
    // expose feedback + a way to clear it
    feedback,
    setFeedback,
  };

  return (
    <ListContext.Provider value={contextValue}>
      {props.children}
    </ListContext.Provider>
  );
};
