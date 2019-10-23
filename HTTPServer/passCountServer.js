// Include http module.
var http = require('http');
const url = require('url');


// Create http server.
var httpServer = http.createServer(function (req, resp) {
  
  const currentUrl = url.parse(req.url);
  
  params = new URLSearchParams( currentUrl.search );
  
  let sensorData = {};
  sensorData.coachnumber = params.get("coachnumber"); 
  sensorData.vehiclenumber = params.get("vehiclenumber");
  sensorData.filledSeats = params.get("filledSeats");

  console.log( sensorData );

  resp.writeHeader(200);

  resp.end('Received data ' + JSON.stringify(sensorData));//  + sensorData);
});

// Http server listen on port 8888.
httpServer.listen(8080);