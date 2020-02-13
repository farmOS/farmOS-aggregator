declare global {
  interface Window { _env: any; }
}

window._env = window._env || {};

export function env(key = '') {
  return window._env[key];
}
