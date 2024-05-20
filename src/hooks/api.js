import axios from 'axios'

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    withCredentials: true,
})

// api.interceptors.request.use(config => {
//     const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
//   if (token) {
//     config.headers['X-CSRFToken'] = token;
//   }
//   return config;
// })

export default api