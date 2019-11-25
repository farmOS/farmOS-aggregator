import axios from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate } from './interfaces';
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
      api_token: apiToken,
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

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  // Farm APIs
  async getFarms(token: string) {
    return axios.get<FarmProfile[]>(`${apiUrl}/api/v1/farms/`, authHeaders(token));
  },
  async updateFarm(token: string, farmId: number, data: FarmProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/farms/${farmId}`, data, authHeaders(token));
  },
  async createFarm(token: string, data: FarmProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/farms/`, data, authHeaders(token));
  },
  async authorizeFarm(token: string, farmID: number, data: FarmProfileAuthorize, apiToken?: string) {
    const headers = authHeaders(token, apiToken);
    return axios.post(`${apiUrl}/api/v1/utils/authorize-farm/${farmID}`, data, headers);
  },
  async createFarmAuthLink(token: string, farmID: number) {
    return axios.post(`${apiUrl}/api/v1/utils/farm-auth-link/${farmID}`, null, authHeaders(token));
  },
  async getOneFarm(token: string, farmID: number, apiToken?: string ) {
    return axios.get<FarmProfile>(`${apiUrl}/api/v1/farms/${farmID}`, authHeaders(token, apiToken));
  },
  async getFarmInfo(token: string, farmID: number) {
    const params = new URLSearchParams();
    params.append('farm_id', farmID.toString());
    return axios.get(
        `${apiUrl}/api/v1/farms/info/`,
        {params, headers: authHeaders(token).headers},
    );
  },
  // Anonymous User Farm APIs

};
