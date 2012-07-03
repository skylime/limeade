/**
 * A WebSocket to TCP socket proxy
 * Creates a new proxy for every TCP connection.
 *
 * Required node modules: ws, base64 and policyfile
 */

var net = require('net'),
    http = require('http'),
    url = require('url'),
    policyfile = require('policyfile'),
    
    base64 = require('base64/build/Release/base64'),
    Buffer = require('buffer').Buffer,
    WebSocketServer = require('ws').Server,
    
    wsServer, token, params, options, django_url, http_server, proxy_server,
    instance_id, http_request, source_host, source_port, target_port, 
    target_host, data = null,
    
    web_host = '127.0.0.1',
    web_port = 8000,
    instances = [];

/**
 * Handle new Client WebSocket connection
 */
new_client = function(client) {
    var vnc = net.createConnection(target_port,target_host);
    console.log('   - WebSocket client connected.');
    
    vnc.on('begin', function() {
        console.log((new Date()) + ' connected to target');
    });
    
    vnc.on('data', function(data) {
        client.send(base64.encode(new Buffer(data)));
    });
    
    vnc.on('end', function() {
        console.log((new Date()) + ' target disconnected');
    });
    
    client.on('message', function(msg) {
        vnc.write(base64.decode(msg), 'binary');
    });
    
    client.on('close', function(code, reason) {
        console.log((new Date()) + ' WebSocket client disconnected: ' + code + ' [' + reason + ']');
    });
    
    client.on('error', function(e) {
        console.log((new Date()) + ' WebSocket client error: ' + e);
    });
};

proxy_request = function(req, res) {
    console.log((new Date()) + ' New proxy request');
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('OK');
};

proxy_server = http.createServer(proxy_request);

function start_new_proxy(shost, sport, thost, tport)
{
    proxy_server.listen(sport, function() {
        console.log('WebSocket settings: ');
        console.log('   - proxing from ' + shost + ':' + sport + ' to ' + thost + ':' + tport);
        wsServer = new WebSocketServer({
            server: proxy_server
        });
        wsServer.on('connection', new_client);
    });
    // Attach Flash policyfile answer service.
    policyfile.createServer().listen(-1, proxy_server);
}

function send_data_to_client(res, chunk, instance_id)
{
    // parse data
    data = JSON.parse(chunk);
    source_host = data.source_host;
    source_port = data.source_port;
    target_host = data.target_host;
    target_port = data.target_port;
    
    // get response back to template
    res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });
    res.write(chunk);
    res.end();
    
    // check if we have a running instance, if not start new proxy
    if (instances.indexOf(instance_id) == -1) {
        // push data to array
        instances.push(instance_id);
        instances[instance_id] = [];
        instances[instance_id].push(data);
        
        start_new_proxy(source_host, source_port, target_host, target_port);
    }
}

function receive_data(req, res)
{
    params = url.parse(req.url, true, false);
    instance_id = params.query.instance_id;
    token = params.query.token;
    django_url = params.query.url;
    
    console.log((new Date()) + ' Try to get VNC data from: ' + django_url);
    
    options = {
        host: web_host,
        port: web_port,
        path: django_url
    };
    
    var request = http.request(options, function(response) {
        if (response.statusCode == 200) {
            // if HTTP status = 200 procceed with operation
            console.log((new Date()) + ' received Status Code ' + response.statusCode);
            response.setEncoding('utf8');
            response.on('data', function(chunk) {
                console.log((new Date()) + ' Data recieved.');
                send_data_to_client(res, chunk, instance_id);
            });
        } else {
            // else don't break and get information back to browser
            console.log((new Date()) + ' received Status Code ' + response.statusCode + ' Maybe permission denied.');
            response.setEncoding('utf8');
            response.writeHead(200,{
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'
            });
            response.write('Permission denied.');
            response.end();
        }
    });
    
    request.on('error', function(e) {
        console.log((new Date()) + ' Problem with request: ' + e.message);
    });
    
    request.end();
}

http_request = function(req, res) {
    console.log((new Date()) + ' Request from: ' + url.parse(req.url).pathname);
    receive_data(req, res);
};

http_server = http.createServer(http_request);

http_server.listen(6008, function() {
    console.log((new Date()) + ' Server is listening on port 6008');
});

