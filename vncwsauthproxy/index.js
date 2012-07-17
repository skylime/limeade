/**
 * A Websocket to TCP proxy in node.js.
 *
 * know to work with node.js 0.6.* and 0.8.*
 *
 * required modules: ws, policyfile
 *     $ npm install ws policyfile
 */

// require needed node modules
var WebSocketServer = require('ws').Server;
var policyfile      = require('policyfile');
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

// define logging settings
var Logging = {};

Logging._log_level = 'debug';
Logging.init_logging = function(level) {
    if (typeof level === 'undefined') {
        level = Logging._log_level;
    } else {
        Logging._log_level = level;
    }
    
    Logging.Debug = Logging.Info = Logging.Warn = Logging.Error = function(msg) {};
    switch (level) {
        case 'debug':
            Logging.Debug = function(msg) { console.log(msg); };
        case 'info':
            Logging.Info = function(msg) { console.log(msg); };
        case 'warn':
            Logging.Warn = function(msg) { console.warn(msg); };
        case 'error':
            Logging.Error = function(msg) { console.error(msg); };
        case 'none':
            break;
        default:
            throw("invalid logging type '" + level + "'");
    }
};

Logging.get_logging = function() {
    return Logging._log_level;
};

Logging.init_logging();


function handleProxy(ws, vncSocket) {
    vncSocket.on('begin', function() {
        // New connection established
        Logging.Debug('Connected to target');
    });
    
    vncSocket.on('data', function(data) {
        // Send data to the client
        ws.send(new Buffer(data).toString('base64'));
    });
    
    vncSocket.on('end', function() {
        // End the websocket connection
        ws.close();
        Logging.Warn('VNC Target disconnected');
    });
    
    ws.on('message', function(msg) {
        // Send data to VNC
        vncSocket.write(new Buffer(msg, 'base64').toString('binary'), 'binary');
    });
    
    ws.on('close', function(code, reason) {
        // End the connection
        vncSocket.end();
        Logging.Warn('WebSocket client disconnected: ' + code + ' [' + reason + ']');
    });
    
    ws.on('error', function(e) {
        // In case of errors, print that out
        Logging.Error('WebSocket client error: ' + e);
    });
}


function connectTarget(host, port, callback) {
    try {
        var vncSocket = net.createConnection(port, host);
        Logging.Info('Client connected to VNC server on ' + host + ':' + port);
        Logging.Info('Start proxying from ' + serverOptions.host + ':' + serverOptions.port + ' to ' + host + ':' + port + "\n");
        callback(vncSocket);
    } catch (e) {
        Logging.Error('Could not create connection to VNC: ' + e.message);
    }
}


function checkValidation(instance_id, session, callback) {
    // make API call on Django
    var options = {
        host: django.host,
        port: django.port,
        path: '/cloud/instance/' + instance_id + '/' + session + '/'
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
            Logging.Warn('Permission denied. Status Code: ' + res.statusCode);
            try {
                res.writeHead(res.statusCode, {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Origin': '*'
                });
                res.write('Permission denied.');
                res.end();
            } catch (e) {
                Logging.Error('Error: ' + e.message);
            }
        }
    });
    
    req.on('error', function(e) {
        Logging.Error('Problem with request: ' + e.message);
    });
    req.end();
}


function extractParams(header, callback) {
    var path        = header.url;
    var cookie      = header.headers.cookie.toString();
    var params      = url.parse(path, true, false);
    var instance_id = params.query.instance_id;
    var session_id  = '';
    
    cookie = cookie.split("; ");
    Logging.Debug('Cookie received: ' + cookie);
    
    for (var i = 0; i < cookie.length; i++) {
        var loc = cookie[i].search(/session/);
        if (loc >= 0) {
            session_id = cookie[i].toString().replace('sessionid=', '');
            Logging.Debug('Session ID: ' + session_id);
        }
    }
    
    if (session_id == '') {
        Logging.Error('No Session ID found in cookie! Use delivered token');
        session_id = params.query.token;
    }
    
    callback(instance_id, session_id);
}


var httpServer = http.createServer(function (request, response) {
    response.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });
    response.end('success');
});


httpServer.listen(serverOptions.port, serverOptions.host, function() {
    Logging.Info('Server is running on ' + serverOptions.host + ':' + serverOptions.port);
    
    var wsServer = new WebSocketServer({
        server: httpServer
    });
    
    // Attach Flash policyfile answer service
    policyfile.createServer().listen(-1, httpServer, function() {
        Logging.Info('Flash policyfile attached.');
    });
    
    wsServer.on('connection', function(ws) {
        Logging.Info('New client tries to connect.');
        // extract params
        extractParams(ws.upgradeReq, function(path, session) {
            // check if request was valid
            checkValidation(path, session, function(host, port) {
                // request is valid, connect to vnc server
                connectTarget(host, port, function(vncSocket) {
                    // after connection, handle interaction
                    handleProxy(ws, vncSocket);
                });
            });
        });
    });
});

