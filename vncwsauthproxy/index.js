// require needed node modules
var WebSocketServer = require('ws').Server;
var policyfile      = require('policyfile');
var base64          = require('base64/build/Release/base64');
var Buffer          = require('buffer').Buffer;
var http            = require('http');
var url             = require('url');
var net             = require('net');

// define where django is running
var django = {
    host: '127.0.0.1',
    port: 8000
}

// define server settings
var serverOptions = {
    host: 'localhost',
    port: 8080
}


function handleProxy(ws, vncSocket) {
    vncSocket.on('begin', function() {
        console.log('Connected to target');
    });
    
    vncSocket.on('data', function(data) {
        ws.send(base64.encode(new Buffer(data)));
    });
    
    vncSocket.on('end', function() {
        console.log('Target disconnected');
    });
    
    ws.on('message', function(msg) {
        vncSocket.write(base64.decode(msg), 'binary');
    });
    
    ws.on('close', function(code, reason) {
        console.log('WebSocket client disconnected: ' + code + ' [' + reason + ']');
    });
    
    ws.on('error', function(e) {
        console.log('WebSocket client error: ' + e);
    });
}

function connectTarget(host, port, callback) {
    var vncSocket = net.createConnection(port, host);
    console.log('Client connected to VNC server on ' + host + ':' + port);
    console.log('Start proxying from ' + serverOptions.host + ':' + serverOptions.port + ' to ' + host + ':' + port + "\n");
    callback(vncSocket);
}

function checkValidation(path, callback) {
    var params      = url.parse(path, true, false);
    var instance_id = params.query.instance_id;
    var token       = params.query.token;
    var uri         = params.query.url;
    
    // make API call on Django
    var options = {
        host: django.host,
        port: django.port,
        path: uri
    }
    
    var req = http.request(options, function(res) {
        if (res.statusCode == 200) {
            // ok, we allowed to make connection
            res.setEncoding('utf8');
            res.on('data', function(chunk) {
                var connectionData = JSON.parse(chunk);
                var host = connectionData.host;
                var port = connectionData.port;
                callback(host, port);
            });
        } else {
            console.log('Permission denied. Status Code: ' + res.statuscode);
            response.setEncoding('utf8');
            response.writeHead(403, {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'
            });
            response.write('Permission denied.');
            response.end();
        }
    });
    
    req.on('error', function(e) {
        console.log('Problem with request: ' + e.message);
    });
    req.end();
}

var httpServer = http.createServer(function (request, response) {
    response.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });
    response.end('success');
});

httpServer.listen(serverOptions.port, serverOptions.host, function() {
    console.log('Server is running on ' + serverOptions.host + ':' + serverOptions.port);
    
    var wsServer = new WebSocketServer({
        server: httpServer
    });
    
    // Attach Flash policyfile answer service
    policyfile.createServer().listen(-1, httpServer, function() {
        console.log('Flash policyfile attached.');
    });
    
    wsServer.on('connection', function(ws) {
        console.log('New client tries to connect.');
        // check if request was valid
        var path = ws.upgradeReq.url;
        checkValidation(path, function(host, port) {
            // request is valid, connect to vnc server
            connectTarget(host, port, function(vncSocket) {
                // after connection, handle interaction
                handleProxy(ws, vncSocket);
            });
        });
    });
});

