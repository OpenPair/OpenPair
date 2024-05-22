import axios from 'axios'
import Cookies from 'js-cookie';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    withCredentials: true,
})

api.interceptors.request.use(config => {
    const token = Cookies.get('csrftoken');
    console.log(token);
    if (token) {
        config.headers['X-CSRFToken'] = token;
    }
    return config;
},
err => Promise.reject(err));


export default api