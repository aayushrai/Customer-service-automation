import Table from './ProductsCheckout';
import Button from '@material-ui/core/Button';
import React from 'react';
import "./Checkout.css";


function Checkout() {
    return (
        <div className="checkout">
            <div className="person__data">
                <div className="person__image">
                    <img src="http://127.0.0.1:8000/media/Faces/2020-10-12-12-54-17/0.jpeg" />
                </div>
                <div className="person__info">
                    <div className="lineone">
                        <div>
                            <label className="label">First Name</label>
                            <br></br>
                            <input type="text" id="fname" name="firstname" placeholder="John" ></input>
                        </div>
                        <div>
                            <label className="label">Last Name</label>
                            <br></br>
                            <input type="text" id="lname" name="lastname" placeholder="Doe" ></input>
                        </div>
                    </div>
                    <div className="linetwo">
                        <div>
                            <label className="label">Contact</label>
                            <br></br>
                            <input type="text" id="contact" name="contact" placeholder="XXX-XXX-XXXX" ></input>
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
                        <input size="53" type="text" id="address" name="address" placeholder="" ></input>
                    </div>
                    <div className="linefour">
                        <div >
                            <label className="label">Number of items</label>
                            <br></br>
                            <input type="text" id="items" name="items" placeholder="" ></input>
                        </div>
                        <div>
                            <label className="label">Final Price</label>
                            <br></br>
                            <input type="text" id="price" name="price" placeholder="" ></input>
                        </div>
                    </div>
                </div>
                <div>
                    <Button variant="contained" color="primary" >
                        Order Now
                    </Button>
                </div>
            </div>
            <Table />
        </div>
    )
}

export default Checkout;
