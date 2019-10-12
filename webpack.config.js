module.exports = {
  mode: 'development',
  entry: './src/js/index.js',
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader'],
        
      },
      {
        test: /\.css$/,
        use: [
          "style-loader",
          {
            loader: "css-loader",
            options: {
              modules: true
            }
          }
        ]
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: ["file-loader"]
      },
      {
        test: /\.(html)$/,
        use: ['html-loader']
      }
    ]
  },
  resolve: {
    extensions: ['.html', '.js', '.jsx']
  },
  output: {
    path: __dirname + './static/',
    publicPath: '/static',
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: './static/',
    clientLogLevel: 'debug',
    port: 8081,
    proxy: {
      "*": {
        target: "http://localhost:8080"
      }
    }
  }
};