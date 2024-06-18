import React, { useEffect } from 'react';
import {
  HashRouter as Router,
  Outlet,
  Route,
  Routes,
} from 'react-router-dom';

import { useDispatch, useSelector } from 'react-redux';
<<<<<<< Updated upstream
import './App.css'
import '../styles/main.scss'
import Settings from '../Settings/Settings.jsx'
import Home from '../home/Home.jsx'
=======
import ProtectedRoute from '../ProtectedRoute/ProtectedRoute.jsx';
import ViteStartup from '../ViteStartup/ViteStartup.jsx';
import LoginPage from '../LoginPage/LoginPage.jsx';
import RegisterPage from '../RegisterPage/RegisterPage.jsx';
import UserPage from '../UserPage/UserPage.jsx';
>>>>>>> Stashed changes
import Sidebar from '../Sidebar/sidebar.jsx'
import About from '../AboutPage/About.jsx'
import Help from '../Help/Help.jsx'
import Contact from '../ContactPage/Contact.jsx'

/* import ProtectedRoute from '../ProtectedRoute/ProtectedRoute.jsx';
* import LoginPage from '../LoginPage/LoginPage.jsx';
* import RegisterPage from '../RegisterPage/RegisterPage.jsx';
 * import UserPage from '../UserPage/UserPage.jsx'; */


const AppLayout = () => (
  <>
  <Sidebar />
  <Outlet />
  </>
);

export default function App() {
  const dispatch = useDispatch();


  useEffect(() => {
    dispatch({ type: 'FETCH_USER' });
  }, [dispatch]);


  return (
    <Router>
      <div>
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
          {/* For protected routes, the view could show one of several things on the same route.
            Visiting localhost:5173/user will show the UserPage if the user is logged in.
            If the user is not logged in, the ProtectedRoute will show the LoginPage (component).
            Even though it seems like they are different pages, the user is always on localhost:5173/user */}
				  {/* <Route
            exact path="/user"
            element={
              <ProtectedRoute>
                <UserPage/>
              </ProtectedRoute>
            }
          />
          <Route
            exact path="/login"
            element=
            {user.id ?
              // If the user is already logged in, 
              // redirect to the /user page
              redirect('/user')
              :
              // Otherwise, show the login page
              <LoginPage />
            }
          />

          <Route
            exact path="/registration"
            element=
            {user.id ?
              // If the user is already logged in, 
              // redirect them to the /user page
              redirect("/user")
              :
              // Otherwise, show the registration page
              <RegisterPage />
            }
          />
 */}

