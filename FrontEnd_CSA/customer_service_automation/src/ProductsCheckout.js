import React, { Component } from 'react';
import './ProductCheckout.css';

class Table extends Component {
   
   
   constructor(props) {
      super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
      this.state = { //state is by default an object
         products:this.props.order
      }
      console.log(this.props.order);
   }
   
   renderTableData() {
    return this.state.products.map((order, index) => {
       console.log(order);
       return (
          <tr key={order.id}>
             <td>{order.order_id}</td>
             <td>{order.product}</td>
             <td>{order.user}</td>
             <td>{order.product_quantity}</td>
          </tr>
       )
    })
 }

 renderTableHeader() {
    
    let header = Object.keys({"Order ID":"","Product":"","User":"","Quantity":""})
    return header.map((key, index) => {
       return <th key={index}>{key.toUpperCase()}</th>
    })
 }

 render() {
    return (
       <div>
          <h1 className='title'>Shopping cart</h1>
          <table className='products'>
             <tbody>
                <tr>{this.renderTableHeader()}</tr>
                {this.renderTableData()}
             </tbody>
          </table>
       </div>
    )
 }
   }
   export default Table;