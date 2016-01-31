var spawn = require('child_process').spawn;
var logFile = '/home/kfatehi/public_html/crawler_logs/current.txt';
var logger = require('./logger')(logFile);

var proc = null;


var print = function(line) {
  if (line && line.length) {
    logger.push(new Date().toLocaleTimeString()+" "+line);
  }
}

var killCrawler = function() {
  proc.kill("SIGKILL");
  print("Sent SIGKILL to Crawler")
}

function startCrawler() {
  proc = spawn('/usr/bin/python', ['Crawler.py'], { env: { PYTHONUNBUFFERED: "yes" } })

  proc.on('exit', function() {
    print('Crawler exited')
    proc = null;
  })

  proc.stderr.on('data', function(buffer) {
    print(buffer.toString().trim());
  })

  proc.stdout.on('data', function(buffer) {
    var line = buffer.toString().trim();
    if (line.match(/Please close manually/) || line.match(/No value in Output buffer/)) {
      killCrawler()
    } else {
      print(line);
    }
  });
}

function watchFunc() {
  if (proc == null) {
    startCrawler();
  }
}

// Checks if proc is running, otherwise starts it
var watchInterval = setInterval(watchFunc, 25000);

process.on('SIGINT', function() {
  print('Supervisor received interrupt.');
  if (proc) {
    clearInterval(watchInterval);
    killCrawler()
  }
  process.exit();
})

watchFunc()

spawn('tail', ['-f', logFile], { stdio: 'inherit' });
