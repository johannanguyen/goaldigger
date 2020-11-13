import { GoogleLogin } from 'react-google-login';
import * as React from 'react';
import { clientSocket } from './Socket';

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

  ChangePage();
}

function ChangePage() {
  location.href = '/HomePage';
  // <button  onclick="ChangePage()">index.html</button>
}

export function GoogleButton() {
  return (
    <div>
      <GoogleLogin
        clientId="791115456005-sqrq5ha01c9bmcbe7c7u6lco4p9l4r1b.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={get_info}
        onFailure={responseGoogle}
        cookiePolicy="single_host_origin"
      />
    </div>
  );
}
