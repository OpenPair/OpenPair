import React, { useEffect } from 'react';
import {
  HashRouter as Router,
  redirect,
  Route,
  Routes,
  Navigate,
  Link
} from 'react-router-dom';

import { useDispatch, useSelector } from 'react-redux';
import './App.css'
import AboutPage from '../AboutPage/About.jsx'
import ContactPage from '../ContactPage/Contact.jsx'
import Settings from '../Settings/Settings.jsx'
/* import ProtectedRoute from '../ProtectedRoute/ProtectedRoute.jsx';
* import LoginPage from '../LoginPage/LoginPage.jsx';
* import RegisterPage from '../RegisterPage/RegisterPage.jsx';
* import UserPage from '../UserPage/UserPage.jsx'; */

export default function App() {
  const dispatch = useDispatch();

  const user = useSelector(store => store.user);

  useEffect(() => {
    dispatch({ type: 'FETCH_USER' });
  }, [dispatch]);


  return (
    <Router>
    <nav>
      <Link to="/">Home</Link>
    <br/>
      <Link to="/about">About</Link>
    <br/>
      <Link to="/contact">Contact</Link>
    <br/>
      <Link to="/settings">Settings</Link>
    <br/>
    </nav>
    
      <div>
        <Routes>
	  <Route
	    path="/about"
	    element={<AboutPage />}
	  />

	  <Route
	    path="/settings"
	    element={<Settings />}
	  />

          <Route
            path="/"
            element={<Navigate replace to="/home"/>}
          />

          <Route
            exact path="/home"
            element=
            {user.id ?
              // If the user is already logged in, 
              // redirect them to the /user page
              redirect("/user")
            :
	     <h1>Heyyyyy there square</h1>
            }
          />
          <Route
            path="/contact"
            element={<ContactPage />}
          />

          {/* If none of the other routes matched, we will show a 404. */}
          <Route
            path="*"
            element={<h1>404 - Not Found</h1>}
          />
        </Routes>
      </div>
    </Router>
  )
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

