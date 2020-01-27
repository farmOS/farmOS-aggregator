const env = process.env.VUE_APP_ENV;

let envApiUrl = '';

if (env === 'production') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}`;
} else if (env === 'staging') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_STAG}`;
} else {
  envApiUrl = `http://${process.env.VUE_APP_DOMAIN_DEV}`;
}

export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;
// tslint:disable-next-line:max-line-length
export const openFarmRegistration: boolean = process.env.VUE_APP_OPEN_FARM_REGISTRATION == null ? false : process.env.VUE_APP_OPEN_FARM_REGISTRATION === 'true';
// tslint:disable-next-line:max-line-length
export const inviteFarmRegistration: boolean = process.env.VUE_APP_INVITE_FARM_REGISTRATION == null ? false : process.env.VUE_APP_INVITE_FARM_REGISTRATION === 'true';
