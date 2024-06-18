import '../styles/main.scss'
import { Input,Button } from 'reactstrap'
export default function Chat(){

  return(
    <>
      <div className="chatBox-container">
	<div className="chatBox-content">
	  Some content here
	</div>
    <div className="bottom-chat-actions">
	  <Input />
	  <Button />
	</div>
    </div>
    </>
  )
}
