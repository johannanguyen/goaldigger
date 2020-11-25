import * as React from 'react';
import { GoogleButton } from '../scripts/GoogleLogin';
import './styles.css';

import { GoogleLogin } from 'react-google-login';
import { clientSocket } from '../scripts/Socket';


const responseGoogle = (response) => {
  console.log('Could not log in: ', response);
};

function get_info(google_user) {
  clientSocket.emit('new google user', {
    id_token: google_user.profileObj.googleId,
    email: google_user.profileObj.email,
    username: google_user.profileObj.name,
    image: google_user.profileObj.imageUrl,
  });
  //ChangeVis();
}

function ChangeVis() {
    const root = document.getElementById('visibility');
    root.style.display = 'none'; 
}


export default function LandingPage() {
  return (
    <div id="visibility">
      <div className="root_container">
        <div className="button_container">
          <GoogleButton />
          {/*<GoogleLogin
            // clientId="1062054290390-k78ra3cikp1topp72a1s8bo02m965adi.apps.googleusercontent.com"
            clientId="1054986958378-occ0i46u818t41nptv82m2ompremrnkh.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={get_info}
            isSignedIn
            onFailure={responseGoogle}
            cookiePolicy="single_host_origin"
          />
          */}
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
    </div>
  );
}
