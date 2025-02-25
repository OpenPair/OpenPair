import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from 'react'
import { Button } from 'reactstrap'
import { Link,Outlet } from 'react-router-dom';
import { BsArrowRight, BsArrowLeft } from "react-icons/bs";
import '../styles/main.scss'

/**
   Basic custom Sidebar Component
*/

export default function Sidebar(){

  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => setIsExpanded(!isExpanded);

  return (
    <div style={{ display: 'flex' }}>
      {/* Sidebar */}
    <div className={`sidebar ${isExpanded ? 'expanded' : ''}`}>
      
      <div className="sidebar-header">
	{isExpanded ? (
	  <BsArrowLeft
	    onClick={toggleExpand}/>
	) : (
	  <BsArrowRight
	    onClick={toggleExpand} />
	)}
      </div>
      <nav>
	<p>New Chat Btn</p>
	<Link to="/">Home</Link>
	<br/>
	<Link to="/about">About</Link>
	<br/>
	<Link to="/contact">Contact</Link>
	<br/>
	<Link to="/settings">Settings</Link>
	<br/>
	<Link to="/help">Help</Link>
	<br/>
      </nav>
    </div>
    
    {/* Main Content */}
    <div className="main-content" style={{ marginLeft: isExpanded ? '300px' : '100px' }}>
      <Outlet/>
    </div>
    </div>
  )
}


