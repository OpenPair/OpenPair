import { useState, useEffect } from 'react'
import reactLogo from '../../assets/react.svg'
import viteLogo from '/vite.svg'
import api from '../../hooks/api'
import axios from 'axios'
import Cookies from 'js-cookie'

function ViteStartup() {
    const [count, setCount] = useState(0)
    const [token, setToken] = useState('')

    const handleClick = async (count) => {
        setCount(count + 1)
        await getToken()
        api.post('/api/session/', {'Test': 'This is NOAA'})
            .then(response => console.log('Alright!', response.data)).catch(err => console.log(err))
    }

    const getToken = async () => {
        try {
            const response = await api.get('/api/get-csrf-token');
            console.log('CSRF Token received:', response.data.csrfToken);
            console.log('Cookies.get', Cookies.get('csrftoken'));
        } catch (error) {
            console.error('Failed to get CSRF token', error);
        }
    };

    const testGet = () => {
        axios.get('/api/test-get/', { withCredentials: true, baseURL: 'http://127.0.0.1:8000' })
            .then(response => {
                console.log('This is the test get. Response:', response.data);
            })
            .catch(err => console.log(err))
    }

    useEffect(() => {
        if (!token) {
            getToken()
        }
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
                <p>
                    Edit <code>src/App.jsx</code> and save to test HMR
                </p>
            </div>
            <div><button onClick={() => getToken()}>This will get the token.</button></div>
            <div><button onClick={() => testGet()}>This is a test GET</button></div>
            <p className="read-the-docs">
                Click on the Vite and React logos to learn more
            </p>
        </>
    )
}

export default ViteStartup;