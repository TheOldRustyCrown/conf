const path = require('path')

module.exports = {
  mode: 'production',
  module: {
    rules: [
      { test: /\.js$/, use: 'babel-loader', exclude: /node_modules/ },
      { test: /\.(png|svg|jpg|gif)$/, use: 'file-loader' }
    ]
  }
}
