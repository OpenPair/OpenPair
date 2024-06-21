import '../styles/main.scss'
import { Input, Button } from 'reactstrap'
import { IoIosSend } from "react-icons/io";
import { useEffect, useState } from 'react';
import api from '../../hooks/api';

export default function Chat() {
  const [query, setQuery] = useState('')
  const [convo, setConvo] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const queryAI = (e) => {
    e.preventDefault()
    setIsLoading(true)
    setConvo([{ id: 'msg_newest', content: [{ text: { value: query } }] }, ...convo])
    const hidden_query = query
    setQuery('')
    // console.log('In queryAI', query);
    api.post('api/query-client/', {
      message: hidden_query
    }).then(response => {
      // console.log(response.data);
      setConvo(response.data)
      setIsLoading(false)
    }).catch(err => {
      console.log(err);
    })
  }

  const isDisabled = () => {
    if (isLoading || query === '') return true
    return false
  }

  const getConversation = () => {
    api.get('api/get-conversation')
      .then(response => {
        console.log(response.data);
        setConvo(response.data)
      }).catch(err => {
        console.log(err);
      })
  }

  useEffect(() => {
    getConversation()
  }, [])

  return (
    <>
      <div className="chatBox-container">
<<<<<<< HEAD
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
=======
        <div className="chatBox-content">
          {convo && convo.toReversed().map((message) => {
            if (message.role === 'assistant') {
              return (<p key={message.id}>
                {message.content[0].text.value}
              </p>)
            }
            return (<p key={message.id}>
              {message.content[0].text.value}
            </p>)
          })}
          {isLoading && (
            <>
              <div className="spinner-grow spinner-grow-sm m-1" role='status'>
                <span className="visually-hidden">Loading...</span>
              </div>
              <div className="spinner-grow spinner-grow-sm m-1" role='status'>
                <span className="visually-hidden">Loading...</span>
              </div>
              <div className="spinner-grow spinner-grow-sm m-1" role='status'>
                <span className="visually-hidden">Loading...</span>
              </div>
            </>
          )}
        </div>
        <form onSubmit={(e) => queryAI(e)}>
          <div className="bottom-chat-actions">
            <Input
              placeholder='What will you ask about?'
              onChange={(e) => setQuery(e.target.value)}
              value={query} />
            <Button
              type='submit'
              disabled={isDisabled()}>
              <IoIosSend />
            </Button>
          </div>
        </form>
      </div>
>>>>>>> origin/feature/chat
    </>
  )
}
