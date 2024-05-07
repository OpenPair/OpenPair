import React, { useEffect } from 'react';
import {
  HashRouter as Router,
  redirect,
  Route,
  Routes,
  Navigate,
} from 'react-router-dom';

import { useDispatch, useSelector } from 'react-redux';
import './App.css'
import ProtectedRoute from '../ProtectedRoute/ProtectedRoute.jsx';
import ViteStartup from '../ViteStartup/ViteStartup.jsx';
import LoginPage from '../LoginPage/LoginPage.jsx';
import RegisterPage from '../RegisterPage/RegisterPage.jsx';
import UserPage from '../UserPage/UserPage.jsx';

function App() {
  const dispatch = useDispatch();

  const user = useSelector(store => store.user);

  useEffect(() => {
    dispatch({ type: 'FETCH_USER' });
  }, [dispatch]);

  return (
    <Router>
      <div>
        {/* <Nav /> */}
        <Routes>
          {/* Visiting localhost:5173 will redirect to localhost:5173/home */}
          <Route
            path="/"
            element={<Navigate replace to="/home"/>}
          />
          {/* For protected routes, the view could show one of several things on the same route.
            Visiting localhost:5173/user will show the UserPage if the user is logged in.
            If the user is not logged in, the ProtectedRoute will show the LoginPage (component).
            Even though it seems like they are different pages, the user is always on localhost:5173/user */}
          <Route
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

          <Route
            exact path="/home"
            element=
            {user.id ?
              // If the user is already logged in, 
              // redirect them to the /user page
              redirect("/user")
              :
              // Otherwise, show the Landing page
              <ViteStartup />
            }
          />

          {/* If none of the other routes matched, we will show a 404. */}
          <Route
            path="*"
            element={<h1>404 - Not Found</h1>}
          />
        </Routes>
        {/* <Footer /> */}
      </div>
    </Router>
  )
}

export default App
