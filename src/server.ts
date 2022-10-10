import express, { json, Request, Response } from 'express';
import morgan from 'morgan';
import cors from 'cors';
import * as CryptoJS from 'crypto-js';

const app = express();
app.use(express.json());
app.use(cors());

const PORT = 5002;
const IP = '127.0.0.1';

app.get('/', (req: Request, res: Response) => {
    // Redirect to login
    res.json({});
});

app.route('/login')
.post((req: Request, res: Response) => {
    res.json({});
})
.get((req: Request, res: Response) => {
    res.json({});
});

app.get('/logout', (req: Request, res: Response) => {
    // Maybe change to post
    res.json({});
});

app.get('/profile', (req: Request, res: Response) => {
    res.json({});
});

app.route('/settings')
.get((req: Request, res: Response) => {
    res.json({});
})
.post((req: Request, res: Response) => {
    res.json({});
});

app.get('/removecomic', (req: Request, res: Response) => {
    // Maybe change to delete?
    res.json({});
});

app.get('/library', (req: Request, res: Response) => {
    res.json({});
});

app.get('/search', (req: Request, res: Response) => {
    res.json({});
});

app.get('/comicinfo', (req: Request, res: Response) => {
    res.json({});
});

app.get('/read', (req: Request, res: Response) => {
    res.json({});
});

app.get('/user', (req: Request, res: Response) => {
    res.json({});
});

// app.get('/viewusers', (req: Request, res: Response) => {
//     res.json({});
// });

app.get('/offline.html', (req: Request, res: Response) => {
    res.json({});
});

app.get('/service-worker.js', (req: Request, res: Response) => {
    res.json({});
});

app.use(morgan('dev'));

const server = app.listen(PORT, IP, () => {
    console.log('Server loaded');
    // Initialise database
});

process.on('SIGINT', () => {
    // Clear any setIntervals or any setTimeouts or any remaining processes
    server.close(() => console.log('Server closed'));
});