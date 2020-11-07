import React, { useState, useEffect } from 'react';
import LandingPage from './LandingPage';
import HomePage from  './HomePage';
import UserProfile from './UserProfile';
import Exercise from '../scripts/Exercise';
import { clientSocket } from '../scripts/Socket';


export default function Content() {
    const [num_users, setNumUsers] = useState(0);

        
    useEffect(() => {
      clientSocket.on("new_user", num_users => {
      setNumUsers(num_users);
      console.log("Received something", num_users);
      });
    });

    
    return(
        <div>
            <LandingPage />
            <HomePage />
            <UserProfile />
            <Exercise />
        </div>
    );
}

