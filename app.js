const express = require('express') // import express library in constant

// express app 
const app = express(); 

// register view engine 
app.set('view engine', 'ejs');
app.set('views', 'Tutor');

// listen for requests 
app.listen(3000); 

app.get('/', (req, res) => {
    // res.send('<p>home page</p>'); 
    res.sendFile('./index.html', {root : __dirname});
});

app.get('/Tutor/Exercises.html', (req, res) => {
    // res.send('<p>home page</p>'); 
    res.sendFile('./Tutor/Exercises.html', {root : __dirname});
});

app.use((req, res) =>{
    res.status(404).sendFile('./404.html', { root: __dirname });
})