var http = require("http");
var _ = require("underscore");

http.createServer(function (request, response) {
    response.writeHead(200, {
        "Content-Type": "text/html"
    });
    response.write("<!DOCTYPE html>\n");
    response.write("<title>Dice Roll</title>\n");
    response.write("<body>\n");

    for (var i = 0; i < 5; i++) {
        // Use underscore to get a random number between 1 and 6
        var randNum = _.random(1, 6);

        response.write("<p>" + randNum + "</p>\n");
    }
    response.write("</body>\n</html>");
    response.end();
}).listen(3000);