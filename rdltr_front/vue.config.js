const path = require('path')

module.exports = {
  configureWebpack: {
    performance: {
      maxEntrypointSize: 400000,
      maxAssetSize: 300000,
    },
  },
  publicPath: '/static/',
  outputDir: path.resolve(__dirname, '../rdltr/dist/static'),
  indexPath: '../index.html',
}
