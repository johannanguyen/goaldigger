import React, { useState, useEffect } from 'react';
import { clientSocket } from './Socket';

export default function Exercise() {
    const [num_users, setNumUsers] = useState(0);

        
    useEffect(() => {
      clientSocket.on("new_user", num_users => {
      setNumUsers(num_users);
      console.log("Received something", num_users);
      });
    });


    return(
        <div>
            <h1>Exercise News Feed</h1>
            <p>Testing socket: num_users</p>
            <p>If num_users is printed, google data will break</p>
            <p>If num_users is not printed, google data is received</p>
            <p>Possibly problem with sockets on multiple .jsx files?</p>
        </div>
    );
}