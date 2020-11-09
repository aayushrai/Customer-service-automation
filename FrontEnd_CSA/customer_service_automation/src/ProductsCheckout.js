import React, { Component } from 'react';
import './ProductCheckout.css';

class Table extends Component {
   
   
   constructor(props) {
      super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
      this.state = { //state is by default an object
         products: [
            { id: 1, Product: 'Sunfeast Nice', Weight: '100 gm', Price: 20},
            { id: 2, Product: 'Peanuts', Weight: '1 Kg', Price: 200},
            { id: 3, Product: 'Amul dark chocolate ', Weight: '150 gm', Price: 220},
            { id: 4, Product: 'Fortune Sunlite Refined Sunflower oil', Weight: '5 Litre', Price: 900},
            { id: 5, Product: 'Dr. Oetker Veg Mayo', Weight: '1 Kg', Price: 160}
         ]
      }
   }

   renderTableData() {
    return this.state.products.map((student, index) => {
       const { id, Product, Weight, Price } = student //destructuring
       return (
          <tr key={id}>
             <td>{id}</td>
             <td>{Product}</td>
             <td>{Weight}</td>
             <td>{Price}</td>
          </tr>
       )
    })
 }

 renderTableHeader() {
    let header = Object.keys(this.state.products[0])
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