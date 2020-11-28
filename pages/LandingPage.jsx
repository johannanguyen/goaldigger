import React, { useState, useEffect } from 'react';
import { GoogleButton } from '../scripts/GoogleLogin';
import './styles.css';


import { CategoryButton } from './CategoryButton'
import ScrollToBottom from 'react-scroll-to-bottom';
import Avatar from '@material-ui/core/Avatar';
import { makeStyles } from '@material-ui/core/styles';
import { GoogleOut } from '../scripts/GoogleLogout';

import { GoogleLogin } from 'react-google-login';
import { clientSocket } from '../scripts/Socket';
import { NavLink } from 'react-router-dom';

export default function LandingPage() {

  //const [goals, setGoals] = useState([]);
  const [user, setUser] = useState({});
  
  const responseGoogle = (response) => {
    console.log('Could not log in: ', response);
  };
  
  function get_info(google_user) {
    //location.href = '/HomePage';//ChangePage();
    clientSocket.emit('new google user', {
      id_token: google_user.profileObj.googleId,
      email: google_user.profileObj.email,
      username: google_user.profileObj.name,
      image: google_user.profileObj.imageUrl,
    });
    //ChangeVis();
  
    const root = document.getElementById('navi');
    root.style.display = 'block';
    getGoogleUserInfo();
    event.preventDefault();
  }
  
  function getGoogleUserInfo() {
      React.useEffect(() => {
        clientSocket.on('google info received', (data) => {
          console.log('Received this in the add goal section: ', data);
          setUser(data);
        });
      });
  }
  
  /*
  function ChangePage() {
    location.href = '/HomePage';
    // <button  onclick="ChangePage()">index.html</button>
  }
  */
  
  //use changevis for when logged in to dispaly the navlink
  /*
  function ChangeVis() {
      const root = document.getElementById('navi');
      root.style.display = 'block'; 
  }
  */


  return (
   <div id="visibility">
      <div className="root_container">
        
        <div id="navi" style={{ display: 'none' }}>
          <NavLink to="/HomePage"> HomePage </NavLink>
          <NavLink to="/UserProfile"> UserProfile </NavLink>
          <NavLink to="/AddGoal"> AddGoal </NavLink>
        </div>
        
        <div className="button_container">
          {/*<GoogleButton />*/}
          <GoogleLogin
            // clientId="1062054290390-k78ra3cikp1topp72a1s8bo02m965adi.apps.googleusercontent.com"
            clientId="1054986958378-occ0i46u818t41nptv82m2ompremrnkh.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={get_info}
            isSignedIn
            onFailure={responseGoogle}
            cookiePolicy="single_host_origin"
          />
        </div>
  
        <div className="content_container">
          <br />
          <br />
          <br />
          <h1>G O A L  D I G G E R</h1>
          <p>Achieve more, together.</p>
          <img src="https://i.ibb.co/PDn92m7/featured-stories.png" />
        </div>
      </div>
      
      <br />
      <br />
      
      <Avatar src={user.image} />
    </div>
  );
}
