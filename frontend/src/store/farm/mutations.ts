import { FarmProfile } from '@/interfaces';
import { FarmState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setFarms(state: FarmState, payload: FarmProfile[]) {
        state.farms = payload;
    },
    setFarm(state: FarmState, payload: FarmProfile) {
        const farms = state.farms.filter((farm: FarmProfile) => farm.id !== payload.id);
        farms.push(payload);
        state.farms = farms;
    },
};

const { commit } = getStoreAccessors<FarmState, State>('');

export const commitSetFarm = commit(mutations.setFarm);
export const commitSetFarms = commit(mutations.setFarms);
