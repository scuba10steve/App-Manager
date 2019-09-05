module.exports = {
  mode: 'development',
  entry: './src/main/js/index.js',
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
    path: __dirname + './src/main/resources/',
    publicPath: '/resources',
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: './src/main/resources/',
    clientLogLevel: 'debug',
    port: 8081,
    proxy: {
      "*": {
        target: "http://localhost:8080"
      }
    }
  }
};