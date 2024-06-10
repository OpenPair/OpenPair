import express from 'express';
import 
  rejectUnauthenticated
 from '../modules/authentication-middleware.js';
import encryptLib from '../modules/encryption.js';
import pool from '../modules/pool.js';
import userStrategy from '../strategies/user.strategy.js';

const router = express.Router();

/**
 * GET route template
 */
router.get('/', rejectUnauthenticated, (req, res) => {
	let querytext = `
	// QUERY GOES HERE
	`;
	pool.query(querytext,[])
	.then((result) => {
		// Code to send goes here
	})
	.catch((error) => {
		console.error("Error in GET", error);
		res.sendStatus(500);
	})
	;
});

/**
 * POST route template
 */
router.post('/', rejectUnauthenticated, (req, res) => {
	let querytext = `
	// QUERY GOES HERE
	`;
	pool.query(querytext,[])
	.then((result) => {
		// Code to send goes here
		res.sendStatus(201)
	})
	.catch((error) => {
		console.error("Error in POST", error);
		res.sendStatus(500);
	})
	;
});

/**
 * PUT route template
 */
router.put('/', rejectUnauthenticated, (req, res) => {
	let querytext = `
	// QUERY GOES HERE
	`;
	pool.query(querytext,[])
	.then((result) => {
		// Code to send goes here
		res.sendStatus(200)
	})
	.catch((error) => {
		console.error("Error in PUT", error);
		res.sendStatus(500);
	})
	;
});

/**
 * DELETE route template
 */
router.delete('/', rejectUnauthenticated, (req, res) => {
	let querytext = `
	// QUERY GOES HERE
	`;
	pool.query(querytext,[])
	.then((result) => {
		// Code to send goes here
		res.sendStatus(200)
	})
	.catch((error) => {
		console.error("Error in DELETE", error);
		res.sendStatus(500);
	})
	;
});

module.exports = router;