// server.js
const express = require("express");
const app = express();


var upload_files = require('multer')();

// .. regular set-up for 'app' ..

app.post('/batch/upload', upload_files.array('source_file[]'), process_upload); 

var Promise = require('bluebird');
var fs = Promise.promisifyAll(require('fs'));
var path = require('path');
var sanitize = require("sanitize-filename");

function process_upload(req, res) {
  if(req.files) { 
    console.log("req.files.length = ", req.files.length);
    console.log("hello")
    var upload_dir='Grab';  //somewhere relevant
    var second_dir='uploads'
    console.log(upload_dir)
    Promise.resolve(req.files)
      .each(function(file_incoming, idx) {
          console.log("  Writing POSTed data :", file_incoming.originalname);
          var sanitized_filename = sanitize(file_incoming.originalname);
          var file_to_save = path.join( upload_dir, sanitized_filename );
          var second_to_save = path.join( second_dir, sanitized_filename );
          console.log("hey I got here")
          return fs
            .writeFileAsync(file_to_save, file_incoming.buffer),fs.writeFileAsync(second_to_save, file_incoming.buffer) 
             
      })
      // .catch() code not included for clarity : Clearly you'll need to do some error checking...
      .then( _ => {
        console.log("Added files : Success");
        return res.sendStatus(200);
      });

  }
  
}

// Serve static files from the public dir
app.use(express.static("public"));

// Start the web server on port 3000
app.listen(3000, () => {
  console.log('Listening on http://localhost:3000');
  console.log('Try visiting http://localhost:3000/hello.html');
});