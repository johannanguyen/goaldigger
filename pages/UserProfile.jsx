import React, { useState, useEffect } from 'react';
import Fab from '@material-ui/core/Fab';
//import { clientSocket } from '../scripts/Socket';
import { clientSocket } from './Socket';
import { GoogleOut } from '../scripts/GoogleLogout';

export default function UserProfile() {
  const [user, setUser] = React.useState([]);
  const [goals, setGoals] = React.useState([]);

  function getGoogleUserInfo() {
    React.useEffect(() => {
      clientSocket.on('google info received', updateGoogleUserInfo);
      return () => {
        clientSocket.off('google info received', updateGoogleUserInfo);
      };
    });
  }

  function updateGoogleUserInfo(data) {
    setUser(data);
  }

  function getGoalInfo() {
    React.useEffect(() => {
      clientSocket.on('user goals', updateGoalInfo);
      return () => {
        clientSocket.off('user goals', updateGoalInfo);
      };
    });
  }

  function updateGoalInfo(data) {
    console.log('Received goal info: ', data);
    setGoals(data);
  }

  function ChangePage() {
    location.href = '/AddGoal';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function GoBack() {
    location.href = '/HomePage';
    // <button  onclick="ChangePage()">index.html</button>
  }

  getGoogleUserInfo();
  getGoalInfo();

  return (
    <div className="root_container">
      <GoogleOut/>
      {/*
      <Button
        variant="contained"
        size="large"
        color="white"
        onClick={GoBack}
        style={{
          backgroundColor: '0e99b6', minHeight: '60px', minWidth: '170px', border: '1px solid white',
        }}
      >
        Back
      </Button>
      */}
      <div className="content_container">
        <h1>{user.username}</h1>
        <br />

        <img src={user.image} />
        <br />
        <br />
        {/*
        <Button
          variant="contained"
          size="large"
          color="white"
          onClick={ChangePage}
          style={{
            backgroundColor: '0e99b6', minHeight: '60px', minWidth: '170px', border: '1px solid white',
          }}
        >
          Add Goal
        </Button>
        */}

        <h3>Here's a list of my goals:</h3>
        <div className="goal_container">
          { goals.map((data, index) => (
            <div>
              <b>
                {data.progress}
                :
              </b>
              {' '}
              {data.description}
              <br />
                <Button
                  variant="contained"
                  color="primary"
                  onClick={deleteHandler}
                  style={{ backgroundColor: '0e99b6' }}
                >
                  Delete!
                </Button>
              <br />
              <Button
                  variant="contained"
                  color="primary"
                  onClick={completeHandler}
                  style={{ backgroundColor: '0e99b6' }}
                >
                  Compelete!
                </Button>
              <br />
            </div>
          ))}
        </div>
      </div>
      <div align="right">
        <Fab color="primary" size="small" style={{ backgroundColor: '0e99b6' }}>
          +
        </Fab>
      </div>
    </div>
  );
}
