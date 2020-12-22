process.env.VUE_APP_VERSION = require('../package.json').version

export const URL =
    process.env.VUE_APP_VERSION === 'serve'
    ? '/'
    : 'http://127.0.0.1:5000/'
