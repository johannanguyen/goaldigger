import { clientSocket } from './Socket';
import GoogleLogin from 'react-google-login';
import * as React from 'react';


const responseGoogle = (response) => {
  console.log("Could not log in: ", response);
}

function get_info(google_user) {
    let name = google_user.profileObj.name;
    let google_id = google_user.profileObj.email;
    let image = google_user.profileObj.imageUrl;
    let is_signed_in = google_user.isSignedIn()
    
    clientSocket.emit('google_user', {
        'name': name,
        'google_id': google_id,
        'image': image,
        'is_signed_in': is_signed_in
    });
}

export function GoogleButton() {
    return (
        <div>
            <GoogleLogin
            clientId="926047747876-uprudtkm1e9d6e23nrf252dq07qb62tn.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={get_info}
            onFailure={responseGoogle}
            cookiePolicy={'single_host_origin'}
            />
        </div>
    );
}
