var fs = require('fs');

module.exports = function(filePath) {
  var fd = fs.openSync(filePath, 'w+')

  var truncate = function() {
    fs.ftruncateSync(fd, 0)
    fs.writeSync(fd, "Truncated in order to avoid hitting disk space quota...\n")
  }

  setInterval(truncate, 5 * 60 * 1000) // 5 mins
  truncate();

  return {
    push: function(line) {
      fs.writeSync(fd, line+"\n")
    }
  }
}
