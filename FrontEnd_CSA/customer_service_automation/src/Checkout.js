import Table from './ProductsCheckout';
import Button from '@material-ui/core/Button';
import React, { useState } from 'react';
import "./Checkout.css";
import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect } from 'react';
const url = "http://127.0.0.1:8000";
function Checkout() {
    const [OrderData,setOrder] = useState([]);
    const params = useParams();
    useEffect(() => {
        fetch(url+'/order/'+ params.order_id)
              .then((response) => {
               //  console.log(response.json());
                return response.json();
               })
               .then((data)=>{
                 setOrder(data);
                // console.log("order",data);
               });
               OrderData.map((item)=>{
            })
  
        }, [])
       
        
    return (
        <div className="checkout">
            <div className="person__data">
                <div className="person__image">
                    <img src={OrderData.length &&  url+OrderData[0].user_image} />
                </div>
                <div className="person__info">
                    <div className="order__id">
                        <label className="label">Order Id</label>
                        <br></br>
                        <input type="text" id="orderid" name="Order" value={params.order_id} size="33" readOnly></input>
                    </div>
                    <div className="lineone">
                        <div>
                            <label className="label">Customer Name</label>
                            <br></br>
                            <input type="text" id="fname" name="firstname" value={OrderData.length &&  OrderData[0].user_name} ></input>
                        </div>
                        <div>
                            <label className="label">Customer Email</label>
                            <br></br>
                            <input type="text" id="email" name="firstname" value={OrderData.length &&  OrderData[0].user_email} ></input>
                        </div>
                    </div>
                    <div className="linetwo">
                        <div>
                            <label className="label">Contact</label>
                            <br></br>
                            <input type="text" id="contact" name="contact" value={OrderData.length &&  OrderData[0].user_phone} ></input>
                        </div>
                        <div>
                            <label className="label">Payment Method</label>
                            <br></br>
                            <select name="payment" id="payment">
                                <option value="cash">Cash</option>
                                <option value="card">Card</option>
                                <option value="wallet">Online Wallet</option>
                                <option value="Scan">Scan and pay</option>
                            </select>
                        </div>
                    </div>
                    <div className="linethree">
                        <label className="label">Address</label>
                        <br></br>
                        <input size="53" type="text" id="address" name="address" value={OrderData.length &&  OrderData[0].user_address} ></input>
                    </div>
                    <div className="linefour">
                        <div >
                            <label className="label">Number of items</label>
                            <br></br>
                            <input type="text" id="items" name="items" value={OrderData.length -1} ></input>
                        </div>
                        <div>
                            <label className="label">Final Price</label>
                            <br></br>
                            <input type="text" id="price" name="price" value={params.total} ></input>
                        </div>
                    </div>
                </div>
                <div>
                    <Button variant="contained" color="black" >
                        Order Now
                    </Button>
                </div>
            </div>
            {OrderData.length > 0 &&
                <Table order={OrderData}/>
                 }
        
        </div>
    )
}

export default Checkout;
