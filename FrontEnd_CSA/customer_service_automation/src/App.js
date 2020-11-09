import React, { useEffect, useState } from 'react';
import Header from './Header';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import FaceRecog from "./FaceRecog";
import Checkout from './Checkout';
import ProductSelect from './ProductSelect';
const url = "http://127.0.0.1:8000";


function App() {
  const [FaceDetected,setFaceDetected] = useState([]);

useEffect(() => {
  const interval = setInterval(
    () => {
      fetch(url+"/userdata")
            .then((response) => {
             //  console.log(response.json());
              return response.json();
             })
             .then((data)=>{
               setFaceDetected(data);
               // console.log(data);
             })}
    , 1000);
  return () => {
    clearInterval(interval);
  };
}, []);


      return (
        <Router>
        <div className="App">
          
          <Switch>
              <Route path="/checkout/:order_id">
                <Header />
                <Checkout />
              </Route>
              <Route path="/productselect/:uid">
                <Header />
                <ProductSelect />
              </Route>
              <Route path="/">
                <Header />
                <div className="front">
                  <div>
                    <img src={url+"/video"}></img>
                  </div>
                  <div className="App__container">
                    <div className="App__list">
                      {
                        FaceDetected.map((item,i)=> 
                        <FaceRecog key={i} name={item.user_name} address={item.user_address} path={url+item.user_image} phone={item.user_phone} uid={item.user_id}/>
                    
                        )}
                        </div>
                    </div>
                  </div>
    
              </Route>
            </Switch>
          </div>
          
      </Router>
      );
    }
    
    export default App;
    