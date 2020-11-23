import React, { useState, useEffect } from 'react';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
//import { clientSocket } from '../scripts/Socket';
import { clientSocket } from './Socket';
import { GoogleOut } from '../scripts/GoogleLogout';

export default function AddGoal() {
  const [users, setUsers] = React.useState([]);
  const [category, setCategory] = useState('');
  const [goal, setGoal] = useState('');
  const [progress, setProgress] = useState('');
  const [postText, setPostText] = useState('');

  function getGoogleUserInfo() {
    React.useEffect(() => {
      clientSocket.on('google info received', (data) => {
        console.log('Received this in the add goal section: ', data);
        setUsers(data);
      });
    });
  }

  getGoogleUserInfo();

  const useStyles = makeStyles((theme) => ({
    formControl: {
      margin: theme.spacing(1),
      minWidth: 300,
    },
    selectEmpty: {
      marginTop: theme.spacing(2),
    },
  }));

  const changeHandler_category = (event) => {
    setCategory(event.target.value);
  };

  const changeHandler_goal = (event) => {
    setGoal(event.target.value);
  };

  const changeHandler_postText = (event) => {
    setPostText(event.target.value);
    setProgress('Added');
    //ChangePage();
  };

  function ChangePage() {
    location.href = '/UserProfile';
    // <button  onclick="ChangePage()">index.html</button>
  }

  const clickHandler = () => {
    clientSocket.emit('add_goal', {
      category, goal, progress, postText, users,
    });
    setGoal('');
    setPostText('');
    console.log('sent added goal to server: ', category, goal, progress, postText, users);
  };
  
  const deleteHandler = () => {
    clientSocket.emit('delete_goal', {
      category, goal, progress, postText, users,
    });
    setGoal('');
    setPostText('');
    console.log('sent deleted goal to server: ', category, goal, progress, postText, users);
  };
  
  const completeHandler = () => {
    clientSocket.emit('complete_goal', {
      category, goal, progress, postText, users,
    });
    setGoal('');
    setPostText('');
    console.log('sent completed goal to server: ', category, goal, progress, postText, users);
  };

  return (
    <div className="root_container">
      <GoogleOut />
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
        Back
      </Button>
      */}
      <div className="content_container">

        <h2>Add Goal</h2>
        <img src={users.image} />
        <br />
        <b>{users.username}</b>
        <br />

        <FormControl className={useStyles().formControl}>
          <InputLabel htmlFor="age-native-simple">Select a Category</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={category}
            onChange={changeHandler_category}
          >
            <MenuItem value="Work">Work</MenuItem>
            <MenuItem value="School">School</MenuItem>
            <MenuItem value="Exercise">Exercise</MenuItem>
            <MenuItem value="Food">Food</MenuItem>
            <MenuItem value="Art">Art</MenuItem>
            <MenuItem value="Lifestyle">Lifestyle</MenuItem>
            <MenuItem value="Finance">Finance</MenuItem>
            <MenuItem value="Misc">Misc</MenuItem>
          </Select>
        </FormControl>
        <br />

        <FormControl className={useStyles().formControl}>
          <TextField
            id="outlined-basic"
            label="Enter your goal"
            value={goal}
            onChange={changeHandler_goal}
          />
          <br />

          <TextField
            id="outlined-basic"
            label="Add a message"
            value={postText}
            onChange={changeHandler_postText}
          />
          <br />

          <Button
            variant="contained"
            color="primary"
            onClick={clickHandler}
            style={{ backgroundColor: '0e99b6' }}
          >
            Add!
          </Button>
          
          <br/>
        </FormControl>
      </div>
    </div>
  );
}
