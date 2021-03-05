import axios from 'axios';
import { env } from '@/env';
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate, ApiKey, ApiKeyCreate, ApiKeyUpdate } from './interfaces';
import { FarmProfile, FarmProfileCreate, FarmProfileUpdate, FarmProfileAuthorize } from './interfaces';

function accessTokenAuthHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

function apiTokenAuthHeaders(apiToken: string) {
  return {
    headers: {
      'api-token': apiToken,
    },
  };
}

function authHeaders(token?: string, apiToken?: string) {
  let headers = { headers: {} };
  if (apiToken) {
    headers = apiTokenAuthHeaders(apiToken);
  }
  if (token) {
    headers = accessTokenAuthHeaders(token);
  }
  return headers;
}

export const api = {
  async logInGetToken(username: string, password: string, scope: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    params.append('scope', scope);

    return axios.post(`${env('apiUrl')}/api/v2/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${env('apiUrl')}/api/v2/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${env('apiUrl')}/api/v2/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${env('apiUrl')}/api/v2/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${env('apiUrl')}/api/v2/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${env('apiUrl')}/api/v2/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${env('apiUrl')}/api/v2/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${env('apiUrl')}/api/v2/reset-password/`, {
      new_password: password,
      token,
    });
  },
  // Farm APIs
  async getFarms(token: string) {
    return axios.get<FarmProfile[]>(`${env('apiUrl')}/api/v2/farms/`, authHeaders(token));
  },
  async updateFarm(token: string, farmId: number, data: FarmProfileUpdate) {
    return axios.put(`${env('apiUrl')}/api/v2/farms/${farmId}`, data, authHeaders(token));
  },
  async createFarm(token: string, data: FarmProfileCreate, apiToken?: string) {
    return axios.post(`${env('apiUrl')}/api/v2/farms/`, data, authHeaders(token, apiToken));
  },
  async authorizeFarm(token: string, farmID: number, data: FarmProfileAuthorize, apiToken?: string) {
    const headers = authHeaders(token, apiToken);
    return axios.post(`${env('apiUrl')}/api/v2/utils/authorize-farm/${farmID}`, data, headers);
  },
  async authorizeNewFarm(token: string, farmUrl: string, data: FarmProfileAuthorize, apiToken?: string) {
    const headers = authHeaders(token, apiToken);
    return axios.post(
        `${env('apiUrl')}/api/v2/utils/authorize-farm/`,
        {farm_url: farmUrl, auth_params: data},
        headers);
  },
  async createFarmAuthLink(token: string, farmID: number) {
    return axios.post(`${env('apiUrl')}/api/v2/utils/farm-auth-link/${farmID}`, null, authHeaders(token));
  },
  async sendFarmAuthorizationEmail(token: string, farmID: number, emailTo: string) {
    return axios.post(`${env('apiUrl')}/api/v2/utils/send-farm-authorization-email/?email_to=${emailTo}&farm_id=${farmID}`, null, authHeaders(token));
  },
  async createFarmRegistrationLink(token: string) {
    return axios.post(`${env('apiUrl')}/api/v2/utils/farm-registration-link`, null, authHeaders(token));
  },
  async sendFarmRegistrationEmail(token: string, emailTo: string) {
    return axios.post(
        `${env('apiUrl')}/api/v2/utils/send-farm-registration-email/?email_to=${emailTo}`,
        null,
        authHeaders(token));
  },
  async getOneFarm(token: string, farmID: number, apiToken?: string ) {
    return axios.get<FarmProfile>(`${env('apiUrl')}/api/v2/farms/${farmID}`, authHeaders(token, apiToken));
  },
  async getFarmInfo(token: string, farmID: number) {
    const params = new URLSearchParams();
    params.append('farm_id', farmID.toString());
    return axios.get(
        `${env('apiUrl')}/api/v2/farms/info/?use_cached=false`,
        {params, headers: authHeaders(token).headers},
    );
  },
  async validateFarmUrl(token: string, farmUrl: string, apiToken?: string) {
    const headers = authHeaders(token, apiToken);
    return axios.post(
        `${env('apiUrl')}/api/v2/utils/validate-farm-url`,
        {farm_url: farmUrl},
        headers,
    );
  },
  // Aggregator API Key APIs
  async getApiKeys(token: string) {
    return axios.get<ApiKey[]>(`${env('apiUrl')}/api/v2/api-keys/`, authHeaders(token));
  },
  async createApiKey(token: string, data: ApiKeyCreate) {
    return axios.post(`${env('apiUrl')}/api/v2/api-keys/`, data, authHeaders(token));
  },
  async updateApiKey(token: string, id: number, data: ApiKeyUpdate) {
    return axios.put(`${env('apiUrl')}/api/v2/api-keys/${id}`, data, authHeaders(token));
  },
  async deleteApiKey(token: string, id: number) {
    return axios.delete(`${env('apiUrl')}/api/v2/api-keys/${id}`, authHeaders(token));
  },
};
