import React, { useState, useEffect } from 'react';
import { clientSocket } from '../scripts/Socket';

export default function UserProfile() {
    const [name, setName] = useState("Default name");
    const [googleId, setGoogleId] = useState("Default id");
    const [image, setImage] = useState("Default image")


    useEffect(() => {
        clientSocket.on("google_user", (data) => {
            setName(data.name);
            setGoogleId(data.google_id);
            setImage(data.image);
            console.log("Received something", data);
      });
    });
    

    return(
        <div>
            <h1>User Profile</h1>
            <p>NAME: {name}</p>
            <p>GOOGLEID: {googleId}</p>
            <p>IMAGE: {image}</p>
        </div>
    );
}

