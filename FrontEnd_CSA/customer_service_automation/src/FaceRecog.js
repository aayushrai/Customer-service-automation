import React from 'react';
import "./FaceRecog.css";
import Button from '@material-ui/core/Button';
import { Link } from "react-router-dom";


function FaceRecog({name,address,path,phone,email,uid,index}) {
  const unknownHandler = (index) => {
    if (index==0) {
      return(
        <div className="FaceRecog">
        <img className="FaceRecog__image" src={path}></img>
        <div className="FaceRecog__details">
          <div className="FaceRecog__text">
            <div className="FaceRecog__name"><span style={{color:"grey"}}>Name: </span>{name}</div>
            <div className="FaceRecog__address"><span style={{color:"grey"}}>Address: </span>{address}</div>
            <div className="FaceRecog__phone"><span style={{color:"grey"}}>Contact: </span>{phone}</div>
            <div className="FaceRecog__email"><span style={{color:"grey"}}>Email: </span>{email}</div>
          </div>
            <div className="FaceRecog__button">
            <Link to={"/enroll"}>
              <Button variant="contained" color="primary" >
                Add Unknown
              </Button>
            </Link>
            </div>
        </div>
    </div>
      ) ;
    }
    return(
    <div className="FaceRecog">
    <img className="FaceRecog__image" src={path}></img>
    <div className="FaceRecog__details">
      <div className="FaceRecog__text">
        <div className="FaceRecog__name"><span style={{color:"grey"}}>Name: </span>{name}</div>
        <div className="FaceRecog__address"><span style={{color:"grey"}}>Address: </span>{address}</div>
        <div className="FaceRecog__phone"><span style={{color:"grey"}}>Contact: </span>{phone}</div>
        <div className="FaceRecog__email"><span style={{color:"grey"}}>Email: </span>{email}</div>
      </div>
      <div className="FaceRecog__button">
        <Link to={"/productselect/"+uid}>
          <Button variant="contained" color="primary" >
            Verify Customer
          </Button>
        </Link>
      </div>
    </div> 
</div>
);
  };
    return (
     unknownHandler(index)
    )
}

export default FaceRecog
