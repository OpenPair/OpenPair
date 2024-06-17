import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from 'react'
import { Button } from 'reactstrap'
import { Offcanvas, OffcanvasBody, OffcanvasHeader } from 'reactstrap'
import { BsArrowRight, BsArrowLeft } from "react-icons/bs";
import '../styles/main.scss'
import Chat from '../Chat/Chat.jsx'

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
      <p>This is a custom sidebar component.</p>
    </div>
    
    {/* Main Content */}
    <div className="main-content" style={{ marginLeft: isExpanded ? '300px' : '100px' }}>
      <Chat />
    </div>
    </div>

    
  )
}


