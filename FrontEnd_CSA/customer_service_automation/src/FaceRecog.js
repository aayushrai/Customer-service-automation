import React from 'react';
import "./FaceRecog.css";
function FaceRecog({name,address,path}) {
    return (
      <div className="FaceRecog">
          <img className="FaceRecog__image" src={path}></img>
          <div className="FaceRecog__details">
            <div className="FaceRecog__name">{name}</div>
            <div className="FaceRecog__address">{address}</div>
            
          </div>
      </div>
    )
}

export default FaceRecog
