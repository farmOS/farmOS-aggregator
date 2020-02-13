// Set the apiUrl to the same variable used to configure backend.
const apiUrl = '${SERVER_HOST}';

// General Aggregator config.
const appName = '${AGGREGATOR_NAME}';
const openFarmRegistration = '${AGGREGATOR_OPEN_FARM_REGISTRATION}' === 'true';
const inviteFarmRegistration = '${AGGREGATOR_INVITE_FARM_REGISTRATION}' === 'true';

const oauthClientId = '${AGGREGATOR_OAUTH_CLIENT_ID}';

// Optional Client Secret. Null if not provided.
let oauthClientSecret = '${AGGREGATOR_OAUTH_CLIENT_SECRET}';
if (oauthClientSecret === '') {
  oauthClientSecret = null;
}

// OAuth Scope Config.
let oauthScopes = '${AGGREGATOR_OAUTH_SCOPES}';
if (oauthScopes !== '') {
  oauthScopes = JSON.parse(oauthScopes);
}

// OAuth Scopes that are "checked" by default.
let oauthDefaultScopes = '${AGGREGATOR_OAUTH_DEFAULT_SCOPES}';
if (oauthDefaultScopes !== '') {
  oauthDefaultScopes = JSON.parse(oauthDefaultScopes);
}

// OAuth Scopes that are required by the aggregator.
let oauthRequiredScopes = '${AGGREGATOR_OAUTH_REQUIRED_SCOPES}';
if (oauthRequiredScopes !== '') {
  oauthRequiredScopes = JSON.parse(oauthRequiredScopes);
}

// Assign values to global window.
window._env = {
  apiUrl: apiUrl,
  appName: appName,
  openFarmRegistration: openFarmRegistration,
  inviteFarmRegistration: inviteFarmRegistration,
  oauthClientId: oauthClientId,
  oauthClientSecret: oauthClientSecret,
  oauthScopes: oauthScopes,
  oauthDefaultScopes: oauthDefaultScopes,
  oauthRequiredScopes: oauthRequiredScopes
};
