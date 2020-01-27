import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';
import VuexPersistence from 'vuex-persist';

import { mainModule } from './main';
import { State } from './state';
import { adminModule } from './admin';
import { farmModule } from './farm';

Vue.use(Vuex);

const vuexLocal = new VuexPersistence<State>({
  storage: window.localStorage,
  reducer: (state) => ({
    main: {
      farmAuthorization: state.main.farmAuthorization,
    },
  }),
});

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    admin: adminModule,
    farm: farmModule,
  },
  plugins: [vuexLocal.plugin],
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
