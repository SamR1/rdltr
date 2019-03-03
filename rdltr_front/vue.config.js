const path = require('path')

module.exports = {
  configureWebpack: {
    performance: {
      maxEntrypointSize: 400000,
      maxAssetSize: 300000,
    },
  },
  publicPath: '/',
  outputDir: path.resolve(__dirname, '../rdltr/dist'),
}
