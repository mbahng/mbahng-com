// Not used anymore. Prototype server without express. 

const http = require('http')
const fs = require('fs')  // fs module needed to read external HTML files
const _ = require('lodash')
const port = 3000 

const server = http.createServer(function(req, res) {

    // lodash 
    const num = _.random(0, 20);
    console.log(num);

    // set header content type 
    res.setHeader('Content-Type', 'text/html');

    let path = '.'; 
    switch(req.url) {
        case '': 
            path += '/index.html'; 
            break; 
        case '/favicon.ico': 
            path += '/CSS/favicon/favicon.ico';
            break; 
        case '/': 
            path += '/index.html'; 
            break; 
        case req.url: 
            path += req.url; 
            break; 
        default: 
            path = '404.html'; 
            break; 
    }

    // send a HTML file 
    fs.readFile(path, (error, data) => {
        if (error) {
            console.log(error); 
            res.end(); // ends request
        } else {
            res.write(data); // data is the contents of the html file
            res.end(); // ends request
        }
    })

})

server.listen(port, function(error) {
    if (error) {
        console.log('Something went wrong', error)
    } else {
        console.log('Server is listening on port ' + port)
    }
})