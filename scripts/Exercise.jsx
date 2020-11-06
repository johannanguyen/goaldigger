import React, { useState, useEffect } from 'react';
import ScrollToBottom from 'react-scroll-to-bottom';
import { clientSocket } from './Socket';

export default function Exercise() {
    const [num_users, setNumUsers] = useState(0);
    const [dbName, setDbName] = useState([]);
    const [dbImage, setDbImage] = useState([]);
    const [dbGoal, setDbGoal] = useState([]);
    const [dbStatus, setDbStatus] = useState([]);
    const [dbMessage, setDbMessage] = useState([]);
    
      
    
      useEffect(() => {
        clientSocket.on("goal_history", (data) => {
          setDbName(data["all_names"], []);
          setDbImage(data["all_images"], []);
          setDbGoal(data["all_goals"], []);
          setDbStatus(data["all_statuses"], []);
          setDbMessage(data["all_messages"], []);
          console.log("received something");
        });
      });
      

    useEffect(() => {
      clientSocket.on("new_user", num_users => {
      setNumUsers(num_users);
      console.log("Received something");
      });
    });

    
  return (
    <div>
      <h1>Exercise</h1>
      <p>Placeholder</p>
      Test Number of Users: {num_users}
    </div>
    );
  }
