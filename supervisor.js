var spawn = require('child_process').spawn;

function start() {
  var proc = spawn('/usr/bin/python', ['Crawler.py'], {
    env: {
      PYTHONUNBUFFERED: "yes"
    }
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
      setTimeout(start, 2000);
    } else {
      console.log(line);
    }
  });
}

start();
