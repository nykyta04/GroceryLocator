import { useContext, useState } from 'react'
import React from 'react'; 

import {ListContext} from '../context/ListContext'

const SearchItem = (props) => {
    const {id, itemName} = props.data;

    const { addToList } = useContext(ListContext);
    return(
        <div className='search-item'>
            <p>{itemName}</p>
            <button onClick={() => addToList(id)}>+</button>
        </div>
    )
}

export default SearchItem
