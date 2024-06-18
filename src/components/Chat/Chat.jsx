import '../styles/main.scss'
import { Input,Button } from 'reactstrap'
import { IoIosSend } from "react-icons/io";
export default function Chat(){

  return(
    <>
      <div className="chatBox-container">
	<div className="chatBox-content">
	  Some content here
	  Some more content here as well
	  <br/>
	  Some more content here as well
	</div>
    <div className="bottom-chat-actions">
      <Input id="chat-input" />

      <Button id="send-chat-btn">
	<IoIosSend />
      </Button>

    </div>
    </div>
    </>
  )
}
