const path = require('path')

module.exports = {
  mode: 'production',
  entry: './opendating/static/js/index.js',
  output: {
    path: path.resolve(__dirname, 'opendating/static/dist/js')
  },
}
