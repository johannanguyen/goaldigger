import * as React from 'react';

export default function HomePage() {
    
    function ChangePage() {
        location.href="/second" 
    }
    
    return(
        <div>
            <h1>Home Page</h1>
            <p> Categories on left sidebar, all-inclusive news feed</p>
            <button  onClick={ChangePage}>Go to second page</button>
             <a href="/second">Click me to go to a second page!</a>
        </div>
    );
}
