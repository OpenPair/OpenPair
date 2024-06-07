import { useState, useEffect } from 'react'
import reactLogo from '../../assets/react.svg'
import viteLogo from '/vite.svg'
import api from '../../hooks/api'
import axios from 'axios'
import Cookies from 'js-cookie'

function ViteStartup() {
    const [count, setCount] = useState(0)

    const handleClick = async (count) => {
        setCount(count + 1)
        // await getToken()
        api.post('/api/session/', {'Test': 'There\'s no way this is actually working'})
            .then(response => console.log('Alright!', response.data)).catch(err => console.log(err))
    }

    const getCount = () => {
        api.get('/api/count/')
        .then(response => {
            console.log(response.data);
        }).catch(err => {
            console.log(err);
        })
    }

    useEffect(() => {
        api.post('/api/count/', {count: 'When will this work??'})
        .then((response) => {
            console.log('Set intial count for this session.', response);
            getCount()
        })
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
            <h1>Vite + React</h1>
            <div className="card">
                <button onClick={() => handleClick(count)}>
                    count is {count}
                </button>
                <button onClick={() => getCount()}>Get Count Now.</button>
                <p>
                    Edit <code>src/App.jsx</code> and save to test HMR
                </p>
            </div>
            <p className="read-the-docs">
                Click on the Vite and React logos to learn more
            </p>
        </>
    )
}

export default ViteStartup;
