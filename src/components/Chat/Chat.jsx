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
      console.log('THEN:', response.data);
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

  // I need to search the response text for words in the vocab list (which there should be)
  // Loop through list of words (if there are any), and separate response into an array of objects, tagged as isVocab.
  // Map the array for the message, and if it is vocab, return a span with classes to make a tooltip, and 
  // if it isn't, return a Markdown component.

  return (
    <>
      <div className="chatBox-container">
        <div className="chatBox-content">
          {convo && convo.toReversed().map((message) => {
            const message_string = message.content[0].text.value
            if (message.role === 'assistant') {
              return (
                <AIResponse
                  key={message.id}
                  message={message.content[0].text.value}
                  vocab={message.vocab} />)
            }
            return (<UserResponse key={message.id} message={message_string} />)

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
          <div className="bottom-chat-actions" style={{ padding: '10px', marginBottom: '10px' }}>
            <Input
              placeholder='What will you ask about?'
              onChange={(e) => setQuery(e.target.value)}
              value={query}
              className='rounded-4' />
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
