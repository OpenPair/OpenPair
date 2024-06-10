import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from 'react'
import { Button } from 'reactstrap'
import { Offcanvas, OffcanvasBody, OffcanvasHeader } from 'reactstrap'

import '../styles/main.scss'

export default function Sidebar(){

  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => setIsOpen(!isOpen);

  return(

    <div>
      <Button
	color="primary"
	onClick={toggle}
      >
	Open
      </Button>
      <Offcanvas isOpen={isOpen}
      toggle={toggle}>
	<OffcanvasHeader >
	  Offcanvas
	</OffcanvasHeader>
	<OffcanvasBody>
	  <strong>
            This is the Offcanvas body.
	  </strong>
	</OffcanvasBody>
      </Offcanvas>
    </div>
    
  )
}


