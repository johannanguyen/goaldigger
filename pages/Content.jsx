import React, { Component, useState } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';


import LandingPage from './LandingPage';
import HomePage from './HomePage';
import UserProfile from './UserProfile';
import AddGoal from './AddGoal';

import Exercise from '../scripts/Exercise';
import Art from '../scripts/Art';

export default function Content() {
  /*
  function User() {
    const prof = document.getElementById('prof');
    const home = document.getElementById('home');
    const goal = document.getElementById('goal');
    
    prof.style.display = 'block';
    home.style.display = 'none'; 
    goal.style.display = 'none';
  }
  
  function Home() {
    const prof = document.getElementById('prof');
    const home = document.getElementById('home');
    
    prof.style.display = 'none';
    home.style.display = 'block'; 
  }
  
  function Goal() {
    const prof = document.getElementById('prof');
    const goal = document.getElementById('goal');
    
    prof.style.display = 'none';
    goal.style.display = 'block'; 
  }
  
  //will put landingpage code directly into content.jsx then check if it is visible or not, 
  //depending on that will depend on wheter or not to display the homepage
  
  return (
    <div>
      <LandingPage />
      
      <div id="home">
        <button
          variant="contained"
          size="large"
          color="white"
          onClick={User}
          style={{
            backgroundColor: '0e99b6', minHeight: '60px', minWidth: '170px', border: '1px solid white',
          }}
        >
          User Profile
        </button>
        <HomePage />
      </div>
      
      <div id="prof" style={{ display: 'none' }}>
        <button
          variant="contained"
          size="large"
          color="white"
          onClick={Home}
          style={{
            backgroundColor: '0e99b6', minHeight: '60px', minWidth: '170px', border: '1px solid white',
          }}
        >
         Home
        </button>
        
        <button
          variant="contained"
          size="large"
          color="white"
          onClick={Goal}
          style={{
            backgroundColor: '0e99b6', minHeight: '60px', minWidth: '170px', border: '1px solid white',
          }}
        >
         Goal
        </button>
        
        <UserProfile />
       </div>
      
      <div id="goal" style={{ display: 'none' }}>
        <button
          variant="contained"
          size="large"
          color="white"
          onClick={User}
          style={{
            backgroundColor: '0e99b6', minHeight: '60px', minWidth: '170px', border: '1px solid white',
          }}
        >
          User Profile
        </button>
        <AddGoal />
      </div>
    </div>
  );
  */
  
  //{/*<Route path="/AddGoal" component={AddGoal} />*/}
  return (
    <BrowserRouter>
      <div>
        <Switch>
          <Route path="/Art"> <Art /> </Route> 

          <Route path="/AddGoal"> <AddGoal /> </Route>
          <Route path="/UserProfile"> <UserProfile/> </Route>
          <Route path="/HomePage"> <HomePage/> </Route>
          <Route path="/"> <LandingPage /> </Route>
        </Switch>
      </div>
    </BrowserRouter>
  );
  
}
