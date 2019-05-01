import { FarmState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    farms: (state: FarmState) => state.farms,
    oneFarm: (state: FarmState) => (farmId: number) => {
        const filteredFarms = state.farms.filter((farm) => farm.id === farmId);
        if (filteredFarms.length > 0) {
            return { ...filteredFarms[0] };
        }
    },
};

const { read } = getStoreAccessors<FarmState, State>('');

export const readOneFarm = read(getters.oneFarm);
export const readFarms = read(getters.farms);
