import { useState, useContext } from 'react'
import { useNavigate } from 'react-router';
import React from 'react'; 
import ListItem from '../components/ListItem'
import {ListContext} from '../context/ListContext'
import '../styles/App.css'
import axios from 'axios';
import {ITEMS} from '../items';

const ViewList = () => {
  const { listItems } = useContext(ListContext);
  const items = listItems.items;
  const navigate = useNavigate();

  // A click event handler for the calculate button.
  const calculateButtonClickHandler = async () => {
    const itemNames = []; // An array to store the name of each item currently on the user's grocery list.

    // For each item on the grocery list, add the item's name to the itemNames array.
    for(let i = 0; i < items.length; i++) {
      let itemName = ITEMS[items[i]].itemName;
      itemNames.push(itemName);
    }
    // Used for testing, can be deleted for final deployment.
    //console.log("Sending items:", itemNames);

    // Try catch block to send post request containing itemNames array.
    try {
      // Send post request with axios and store backend response in response variable. The response should be an array of store objects.
      const response = await axios.post(`${import.meta.env.VITE_API_URL}sort-lists/`, {items: itemNames});

      // Assign the store with the lowest total (response.data[0]) to cheapestStore.
      // Send the FULL array of stores (not just the first one)
      navigate('/total', { state: { sortedStores: response.data } });
      //console.log("Store:" , cheapestStore);
      //console.log("Response: ", response.data);
    }
    // Catch error if an error occurs while sending request, display error.
    catch (error) {
      console.error('Error fetching prices: ', error);
    }
  }

  return (
    <div className="list-item-container">
      <h2>Your list:</h2>
      {items.map((item) => (<ListItem key={item} data={item}/>))}
      <button className="calculate-button" onClick={calculateButtonClickHandler}>Calculate!</button>
    </div>
  );
}

export default ViewList
