import { useContext, useState } from 'react'
import React from 'react'; 
import {ITEMS} from '../items'
import {ListContext} from '../context/ListContext'

const ListItem = (props) => {
    const id = props.data;
    var item = ITEMS[id];
    
    const { removeFromList } = useContext(ListContext);
    return(
        <div className='list-item'>
            <p>{item.itemName}</p>
            <button onClick={() => removeFromList(id)}>Delete</button>
        </div>
    )
}

export default ListItem
