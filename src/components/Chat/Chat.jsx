import '../styles/main.scss'
import { Input,Button } from 'reactstrap'
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
      <Input />
      <Button />
    </div>
    </div>
    </>
  )
}
