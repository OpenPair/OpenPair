import express from 'express';
const app = express();
import { config } from 'dotenv';
const PORT = process.env.PORT || 5001;

// Middleware Includes
import sessionMiddleware from './modules/session-middleware.js'
import passport from './strategies/user.strategy.js';

// Route Includes
import userRouter from './routes/user.router.js';

// Express Middleware
app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.use(express.static('build'));

// Passport Session Configuration
app.use(sessionMiddleware);

// Start Passport Sessions
app.use(passport.initialize());
app.use(passport.session());

// Routes
app.use('/api/user', userRouter);

// Listen Server & Port
app.listen(PORT, () => {
  console.log(`Listening on port: ${PORT}`);
});
