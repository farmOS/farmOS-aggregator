import { IUserProfile, ApiKey } from '@/interfaces';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setUsers(state: AdminState, payload: IUserProfile[]) {
        state.users = payload;
    },
    setUser(state: AdminState, payload: IUserProfile) {
        const users = state.users.filter((user: IUserProfile) => user.id !== payload.id);
        users.push(payload);
        state.users = users;
    },
    setApiKeys(state: AdminState, payload: ApiKey[]) {
        state.apiKeys = payload;
    },
    setApiKey(state: AdminState, payload: ApiKey) {
        const keys = state.apiKeys.filter((key: ApiKey) => key.id !== payload.id);
        keys.push(payload);
        state.apiKeys = keys;
    },
    deleteApiKey(state: AdminState, id: number) {
        const i = state.apiKeys.map((item) => item.id).indexOf(id);
        state.apiKeys.splice(i, 1);
    },
};

const { commit } = getStoreAccessors<AdminState, State>('');

export const commitSetUser = commit(mutations.setUser);
export const commitSetUsers = commit(mutations.setUsers);
export const commitSetApiKeys = commit(mutations.setApiKeys);
export const commitSetApiKey = commit(mutations.setApiKey);
export const commitDeleteApiKey = commit(mutations.deleteApiKey);
