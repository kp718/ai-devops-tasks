
const DEFAULT_CONFIG = {
  apiUrl: 'http://localhost:3000/api',
  debug: true,
  timeout: 5000
};

const ENV_CONFIGS = {
  development: DEFAULT_CONFIG,

  testing: {
    apiUrl: 'http://test-server:3000/api',
    debug: true,
    timeout: 5000
  },

  staging: {
    apiUrl: 'https://staging.example.com/api',
    debug: false,
    timeout: 10000
  },

  production: {
    apiUrl: 'https://api.example.com',
    debug: false,
    timeout: 15000
  }
};

function getEnvironmentConfig(env) {
  return ENV_CONFIGS[env] ?? DEFAULT_CONFIG;
}
