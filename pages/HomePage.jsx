import React, { useState, useEffect } from 'react';
import { CategoryButton } from './CategoryButton'
import { makeStyles } from '@material-ui/core/styles';
import Avatar from '@material-ui/core/Avatar';
//import { clientSocket } from '../scripts/Socket';
import { clientSocket } from './Socket';
import { GoogleOut } from '../scripts/GoogleLogout';
import ScrollToBottom from 'react-scroll-to-bottom';

export default function HomePage() {
  const [goals, setGoals] = useState([]);
  const [user, setUser] = useState({});

  const useStyles = makeStyles((theme) => ({
    formControl: {
      margin: theme.spacing(1),
      minWidth: 150,
    },
  }));
  
  function getGoals(){
    React.useEffect(() => {
      clientSocket.on('homepage', updateGoals)
      return () => {
        clientSocket.off('homepage', updateGoals)
      }
    })
  }
  
  function updateGoals(data) {
    setGoals(data)
  }
  
  function getGoogleUserInfo() {
    React.useEffect(() => {
      clientSocket.on('google info received', (data) => {
        console.log('Received this in the add goal section: ', data);
        setUser(data);
      });
    });
  }
  getGoogleUserInfo();
  getGoals();

  function ChangePage() {
    location.href = '/UserProfile';
    // <button  onclick="ChangePage()">index.html</button>
  }
  /*
  function WorkPage() {
    location.href = '/Work';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function SchoolPage() {
    location.href = '/School';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function ExercisePage() {
    location.href = '/Exercise';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function FoodPage() {
    location.href = '/Food';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function ArtPage() {
    location.href = '/Art';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function LifePage() {
    location.href = '/Life';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function FinancePage() {
    location.href = '/Finance';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function MiscPage() {
    location.href = '/Misc';
    // <button  onclick="ChangePage()">index.html</button>
  }

  function GroupsPage() {
    location.href = '/Groups';
    // <button  onclick="ChangePage()">index.html</button>
  }
*/
  // do div box styling for the week

  return (
    <div className="root_container">
      <GoogleOut/>
      <div className="category_menu">
        <br />
        <CategoryButton category="Work" />
        <CategoryButton category="School" />
        <CategoryButton category="Exercise" />
        <CategoryButton category="Food" />
        <CategoryButton category="Art" />
        <CategoryButton category="Lifestyle" />
        <CategoryButton category="Finance" />
        <CategoryButton category="Misc" />
        <CategoryButton category="Groups" />
      </div>

      <div className="header_menu">
        <h2>Home</h2>
        {/*
        <Button
          variant="contained"
          size="large"
          color="primary"
          onClick={ChangePage}
          style={{
            backgroundColor: '0e99b6', minHeight: '60px', minWidth: '170px', border: '1px solid white',
          }}
        >
        
          User Profile
        </Button>
        */}

        <Avatar src={user.image} />
      </div>

      <div className="homepage_container">
        <ScrollToBottom>
        { goals.map((data, index) => (
          <div>
            <Avatar src={data.img_url} />

            {data.name}
            {' '}
            {data.progress}
            {' '}
            a goal in
            {' '}
            <b>{data.category}</b>
            :
            {' '}
            {data.description}
            <br />
            "
            {data.post_text}
            "
          </div>
        )) }
        </ScrollToBottom>
      </div>
    </div>
  );
}
