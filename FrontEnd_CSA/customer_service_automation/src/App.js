import React, { useEffect, useState } from 'react';
import Header from './Header';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import FaceRecog from "./FaceRecog";
import Checkout from './Checkout';
import ProductSelect from './ProductSelect';
import Enroll from './Enroll';
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
    , 3000);
  return () => {
    clearInterval(interval);
  };
}, []);

useEffect(() => {
  const interval = setInterval(
    () => {
      fetch(url+"/applydiscount")
            .then((response) => {
             //  console.log(response.json());
              return response.json();
             })
             .then((data)=>{
               // console.log(data);
             })}
    , 60000);
  return () => {
    clearInterval(interval);
  };
}, []);


      return (
        <Router>
        <div className="App">
          
          <Switch>
              <Route path="/checkout/:order_id/:total">
                <Header />
                <Checkout />
              </Route>
              <Route path="/productselect/:uid">
                <Header />
                <ProductSelect />
              </Route>
              <Route path="/enroll">
                <Header />
                <Enroll />
              </Route>
              <Route path="/">
                <Header />
                <div className="front">
                  <div > 
                    <img className="App__camera" src={url+"/video"}></img>
                  </div>
                  <div className="App__container">
                    <div className="App__list">
                      {
                        FaceDetected.map((item,i)=> 
                        <FaceRecog key={i} name={item.user_name} address={item.user_address} path={url+item.user_image} phone={item.user_phone} uid={item.user_id} index={i}/>
                    
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
    