// serve

const express = require("express");
const app = express();



var upload_files = require('multer')();

// .. regular set-up for 'app' ..

app.post('/batch/upload', upload_files.array('source_file[]'), process_upload); 

var Promise = require('bluebird');
var fs = Promise.promisifyAll(require('fs'));
var path = require('path');
var sanitize = require("sanitize-filename");
let {PythonShell} = require('python-shell');




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
        
          let x = fs
            .writeFileSync(file_to_save, file_incoming.buffer) 
          let y = fs.writeFileSync(second_to_save, file_incoming.buffer)    

      })
    
      .then( _ => {
        console.log("Added files : Success");

        let x = res.sendStatus(200)
        PythonShell.run('C:/Users/jakuz/Documents/13/13/11.3.1-simple-express-web-server/NLPEngine/upload.py', null,  function (err) {
          if (err) throw err;
          console.log('finished');
        });
        setTimeout(function() {
          //your code to be executed after 1 second
          
          const directory = "C:/Users/jakuz/Documents/13/13/11.3.1-simple-express-web-server/Grab/";

          fs.readdir(directory, (err, files) => {
            if (err) throw err;
          
            for (const file of files) {
              // fs.closeSync(file);
              fs.unlink(path.join(directory, file), err => {
                if (err) throw err;
              });
            }
          });
        }, 10000);
      
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