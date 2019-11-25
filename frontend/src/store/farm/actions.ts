import { api } from '@/api';
import { ActionContext } from 'vuex';
import { FarmProfileCreate, FarmProfileUpdate, FarmProfileAuthorize } from '@/interfaces';
import { State } from '../state';
import { FarmState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitSetFarms, commitSetFarm } from './mutations';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';

type MainContext = ActionContext<FarmState, State>;

export const actions = {
    async actionGetFarms(context: MainContext) {
        try {
            const response = await api.getFarms(context.rootState.main.token);
            if (response) {
                commitSetFarms(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateFarm(context: MainContext, payload: { id: number, farm: FarmProfileUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateFarm(context.rootState.main.token, payload.id, payload.farm),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetFarm(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Farm successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateFarm(context: MainContext, payload: FarmProfileCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createFarm(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetFarm(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Farm successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionAuthorizeFarm(
        context: MainContext,
        payload: {id: number, authValues: FarmProfileAuthorize, apiToken?: string }) {
      try {
          const loadingNotification = { content: 'authorizing', showProgress: true };
          commitAddNotification(context, loadingNotification);
          const response = (await Promise.all([
              api.authorizeFarm(context.rootState.main.token, payload.id, payload.authValues, payload.apiToken ),
              await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
          ]))[0];
          commitRemoveNotification(context, loadingNotification);
          commitAddNotification(context, { content: 'Farm authorized.', color: 'success' });
      } catch (error) {
          await dispatchCheckApiError(context, error);
      }
    },
    async actionCreateFarmAuthLink(context: MainContext, payload: {farmID: number}) {
        try {
            const response = await api.createFarmAuthLink(context.rootState.main.token, payload.farmID);
            if (response) {
                return response.data;
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetFarmInfo(context: MainContext, payload: {farmID: number}) {
        try {
            const response = await api.getFarmInfo(context.rootState.main.token, payload.farmID);
            if (response) {
                return response.data[payload.farmID];
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetOneFarm(context: MainContext, payload: { farmID: number, apiToken: string }) {
        try {
            const response = await api.getOneFarm(context.rootState.main.token, payload.farmID, payload.apiToken);
            if (response) {
                return response.data;
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};

const { dispatch } = getStoreAccessors<FarmState, State>('');

export const dispatchCreateFarm = dispatch(actions.actionCreateFarm);
export const dispatchGetFarms = dispatch(actions.actionGetFarms);
export const dispatchUpdateFarm = dispatch(actions.actionUpdateFarm);
export const dispatchAuthorizeFarm = dispatch(actions.actionAuthorizeFarm);
export const dispatchCreateFarmAuthLink = dispatch(actions.actionCreateFarmAuthLink);
export const dispatchGetFarmInfo = dispatch(actions.actionGetFarmInfo);
export const dispatchGetOneFarm = dispatch(actions.actionGetOneFarm);
