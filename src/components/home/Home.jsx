import Chat from '../Chat/Chat.jsx'
import {
  HashRouter as Router,
  redirect,
  Route,
  Routes,
  Navigate,
} from 'react-router-dom';



export default function Home(){
  return(
    <>
    <Chat/>
    </>
    
  )
}
