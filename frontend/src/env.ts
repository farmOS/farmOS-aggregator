declare global {
  interface Window { _env: any; }
}

window._env = window._env || {};

export function env(key = '') {
  // Reloading a page may make the Vue app make an API
  // before knowing the apiURL that is loaded in with a JS file.
  // This allows the window origin to be used in these cases.
  if (window._env[key] === undefined && key === 'apiUrl') {
    return window.location.origin;
  }
  return window._env[key];
}
