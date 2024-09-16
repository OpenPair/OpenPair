import {
  HashRouter as Router,
  redirect,
  Route,
  Routes,
  Navigate,
} from 'react-router-dom';

import { useState, useEffect } from 'react'
import reactLogo from '../../assets/react.svg'
import viteLogo from '/vite.svg'
import api from '../../hooks/api'

const styles = {
    form: {
        margin: 'auto',
        width: '500px',
    },
    assistant: {
        color: 'green',
    },
}

function ViteStartup() {
    const [query, setQuery] = useState('')
    const [convo, setConvo] = useState([])
    const [isLoading, setIsLoading] = useState(false)

    /**
     * A function that calls the query-client endpoint.
     * Sets 'isLoading' to true while we wait for the response.
     * Clears the input field.
     * @param {*} e event
     */
    const queryAI = (e) => {
        e.preventDefault()
        setIsLoading(true)
        // console.log('In queryAI', query);
        api.post('api/query-client/', {
            message: query
        }).then(response => {
            console.log(response.data);
            setConvo(response.data)
            setQuery('')
            setIsLoading(false)
        }).catch(err => {
            console.log(err);
        })
    }

    /**
     * Runs with a useEffect. Gets the whole conversation with the AI without making a run.
     */
    const getConversation = () => {
        api.get('api/get-conversation')
            .then(response => {
                console.log(response.data);
                setConvo(response.data)
            }).catch(err => {
                console.log(err);
            })
    }


    /**
     * A function that determines if the submit button will be disabled or not,
     * depending on if there is something in the input field or if we are waiting
     * for a response from the AI.
     * @returns 
     */
    const isDisabled = () => {
        if (isLoading || query === '') return true
        return false
    }

    useEffect(() => {
        getConversation()
    }, [])

    return (
        <>
            <div>
                <a href="https://vitejs.dev" target="_blank">
                    <img src={viteLogo} className="logo" alt="Vite logo" />
                </a>
                <a href="https://react.dev" target="_blank">
                    <img src={reactLogo} className="logo react" alt="React logo" />
                </a>
            </div>
            <h1>OpenPair</h1>
            <div className="card">
                <form onSubmit={(e) => queryAI(e)} style={styles.form}>
                    <input
                        type="text"
                        placeholder='What will you ask about?'
                        onChange={(e) => setQuery(e.target.value)}
                        value={query} />
                    <button type="submit" disabled={isDisabled()}>Ask</button>
                </form>

            </div>
            <div>
                {convo && convo.toReversed().map((message) => {
                    if (message.role === 'assistant') {
                        return (<p style={styles.assistant} key={message.id}>
                            {message.content[0].text.value}
                        </p>)
                    }
                    return (<p key={message.id}>
                        {message.content[0].text.value}
                    </p>)
                })}
            </div>
        </>
    )
}

export default ViteStartup;
