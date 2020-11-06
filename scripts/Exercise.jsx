import React, { useState, useEffect } from 'react';
import ScrollToBottom from 'react-scroll-to-bottom';
import { clientSocket } from './Socket';

export default function Exercise() {
    const [dbName, setDbName] = useState([]);
    const [dbImage, setDbImage] = useState([]);
    const [dbGoal, setDbGoal] = useState([]);
    const [dbStatus, setDbStatus] = useState([]);
    const [dbMessage, setDbMessage] = useState([]);
    const [num_users, setNumUsers] = useState(0);
      
    
      useEffect(() => {
        clientSocket.on('goal_history', (data) => {
          setDbName(data.all_names, []);
          setDbImage(data.all_images, []);
          setDbGoal(data.all_goals, []);
          setDbStatus(data.all_statuses, []);
          setDbMessage(data.all_messages, []);
          console.log(data);
        });
      });
      
      useEffect(() => {
        clientSocket.on('new_user', (data) => {
          setNumUsers(data.num_users);
          console.log("Received something")
        });
      });

    
      return (
        <div>
             <h1>Exercise</h1>
             <p>Placeholder</p>
        </div>
      );
    }
