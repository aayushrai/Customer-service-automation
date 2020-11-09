import React from 'react';
import "./FaceRecog.css";
import Button from '@material-ui/core/Button';
import { Link } from "react-router-dom";

function FaceRecog({name,address,path,phone,uid}) {
    return (
      <div className="FaceRecog">
          <img className="FaceRecog__image" src={path}></img>
          <div className="FaceRecog__details">
            <div className="FaceRecog__name">{name}</div>
            <div className="FaceRecog__address">{address}</div>
            <div className="FaceRecog__phone">{phone}</div>
          </div>
          <div className="button__apply">
            <Link to={"/productselect/"+uid}>
              <Button variant="contained" color="primary" >
                Verify Customer
              </Button>
            </Link>
          </div>
      </div>
    )
}

export default FaceRecog
