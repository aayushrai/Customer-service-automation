import React, { useState } from 'react';
import './App.css';
import FaceRecog from "./FaceRecog";
const url = "http://127.0.0.1:8000"

function App() {
  const [FaceDetected,setFaceDetected] = useState([]);
  setTimeout(() => {
     fetch(url)
           .then((response) => {
            //  console.log(response.json());
             return response.json();
            })
            .then((data)=>{
              setFaceDetected(data);
              console.log(data);
            })},10000);
      
      const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([{"user_id":"614ffa63-0c67-11eb-bdcf-03b990a51dac","product_id":"5e6eb3cb-e1e0-4e08-aa67-e4198680f841","product_quantity":"2"},{"user_id":"614ffa63-0c67-11eb-bdcf-03b990a51dac","product_id":"11e4e215-2774-48e3-be0c-b6e0276ba690","product_quantity":"1"}])
      };
      fetch('http://127.0.0.1:8000/placeorder', requestOptions)
          .then(response => response.json())
          .then(data => {return { postId: data.id }});

  return (
    <div className="App">
      <h1>welcome</h1>
      <div className="App__container">
      <div className="App__list">
        {
          FaceDetected.map((item,i)=> 
          <FaceRecog key={i} name={item.user_name} address={item.user_address} path={url+item.user_image}/>
       
          )}
          </div>
      </div>
    </div>
  );
}

export default App;
