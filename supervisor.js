var spawn = require('child_process').spawn;

var proc = null;

function startCrawler() {
  proc = spawn('/usr/bin/python', ['Crawler.py'], {
    env: {
      PYTHONUNBUFFERED: "yes"
    }
  })

  proc.on('exit', function() {
    console.log('proc exited');
    proc = null;
  })

  proc.stderr.on('data', function(buffer) {
    var line = buffer.toString().trim();
    console.log(line);
  })

  proc.stdout.on('data', function(buffer) {
    var line = buffer.toString().trim();
    if (line.match(/Please close manually/)) {
      console.log('killing manually...');
      proc.kill("SIGKILL");
    } else {
      console.log(line);
    }
  });
}

function watchFunc() {
  if (proc == null) {
    startCrawler();
  }
}

// Checks if proc is running, otherwise starts it
var watchInterval = setInterval(watchFunc, 2000);

process.on('SIGINT', function() {
  console.log('Supervisor received interrupt.');
  if (proc) {
    clearInterval(watchInterval);
    proc.kill("SIGKILL");
    console.log('Killed subprocess');
  }
  process.exit();
})

watchFunc()
