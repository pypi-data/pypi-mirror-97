const envVars = require('/tmp/hyperglass.env.json');
const { configFile } = envVars;
const config = require(String(configFile));

module.exports = {
  reactStrictMode: true,
  poweredByHeader: false,
  env: {
    _NODE_ENV_: config.NODE_ENV,
    _HYPERGLASS_URL_: config._HYPERGLASS_URL_,
    _HYPERGLASS_CONFIG_: config._HYPERGLASS_CONFIG_,
    _HYPERGLASS_FAVICONS_: config._HYPERGLASS_FAVICONS_,
  },
};
