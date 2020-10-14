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
