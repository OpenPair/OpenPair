import '../styles/main.scss'
import { Input, Button } from 'reactstrap'
import { IoIosSend } from "react-icons/io";
import { useEffect, useState } from 'react';
import AIResponse from '../AIResponse/AIResponse';
import UserResponse from '../UserResponse/UserResponse';
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
        <div className="chatBox-content">
          {convo && convo.toReversed().map((message) => {
            if (message.role === 'assistant') {
              return (
                <AIResponse
                  key={message.id}
                  message={message.content[0].text.value} />)
            }
            return (<UserResponse key={message.id} message={message.content[0].text.value}/>)
  
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
    </>
  )
}
