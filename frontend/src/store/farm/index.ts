import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { FarmState } from './state';

const defaultState: FarmState = {
  farms: [],
};

export const farmModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
