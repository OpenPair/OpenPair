import '../styles/main.scss'
import React, { useEffect } from 'react';
import {
  HashRouter as Router,
  Outlet,
  Route,
  Routes,
} from 'react-router-dom';

import { useDispatch, useSelector } from 'react-redux';
import ViteStartup from '../ViteStartup/ViteStartup.jsx';
import Sidebar from '../Sidebar/sidebar.jsx'
import About from '../AboutPage/About.jsx'
import Help from '../Help/Help.jsx'
import Contact from '../ContactPage/Contact.jsx'
import Home from '../home/Home.jsx'
import Settings from '../Settings/Settings.jsx'


/* import ProtectedRoute from '../ProtectedRoute/ProtectedRoute.jsx';
* import LoginPage from '../LoginPage/LoginPage.jsx';
* import RegisterPage from '../RegisterPage/RegisterPage.jsx';
 * import UserPage from '../UserPage/UserPage.jsx'; */


const AppLayout = () => (
  <>
  <Sidebar />
  </>
);

export default function App() {
  const dispatch = useDispatch();


  useEffect(() => {
    dispatch({ type: 'FETCH_USER' });
  }, [dispatch]);


  return (
    <Router>
      <div className="app-container">
        <Routes>
	  <Route element={<AppLayout />}>
	    <Route path="/" element={<Home />} />
	    <Route path="/settings" element={<Settings />} />
	    <Route path="/about" element={<About />} />
	    <Route path="/help" element={<Help />} />
	    <Route path="/contact" element={<Contact />} />
	  </Route>
        </Routes>
      </div>

    </Router>
  );
}

