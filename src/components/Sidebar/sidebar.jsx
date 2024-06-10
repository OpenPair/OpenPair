import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from 'react'
import { Button } from 'reactstrap'
import { Offcanvas, OffcanvasBody, OffcanvasHeader } from 'reactstrap'
import { BsArrowRight } from "react-icons/bs";

import '../styles/main.scss'

export default function Sidebar(){

  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => setIsExpanded(!isExpanded);

  return (
    <div style={{ display: 'flex' }}>
      {/* Sidebar */}
    <div className={`sidebar ${isExpanded ? 'expanded' : ''}`}>
      
      <div className="sidebar-header">
        <h2>Open Pair</h2>
	<Button>
	<BsArrowRight />
	</Button>
      </div>
      <p>This is a custom sidebar component.</p>
      <button onClick={toggleExpand}>
        {isExpanded ? 'Collapse' : 'Expand'}
      </button>
    </div>
    
    {/* Main Content */}
    <div className="main-content" style={{ marginLeft: isExpanded ? '300px' : '100px' }}>
      <h1>Main Content Area</h1>
      <p>This is the main content area of your application.</p>
    </div>
    </div>

    
  )
}


