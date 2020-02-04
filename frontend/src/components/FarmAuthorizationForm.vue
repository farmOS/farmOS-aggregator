<template>
  <form>
    <div class="headline text--primary">
      farmOS Server Authorization
    </div>
    <div class="subtitle-1 text--primary">
      Authorize your farmOS server with the {{appName}}. This will give the {{appName}} access to your data
      at the level you define.
    </div>
    <br>
    <v-text-field label="farmOS Server URL" v-model="farmUrl" readonly></v-text-field>


    <div class="headline text--primary">
      Permissions
    </div>
    <v-checkbox
      v-for="scope in scopes"
      v-model="oauthScopes"
      v-bind:key="scope.name"
      v-bind:value="scope.name"
      v-bind:label="scope.label"
      v-bind:hint="scope.description"
      :disabled = "requiredScopes.includes(scope.name)"
      persistent-hint
    ></v-checkbox>
  </form>
</template>

<script lang="ts">
    import { apiUrl } from '@/env';
    import oauthConfig from '../oauthConfig.json';
    import { Component, Vue, Prop } from 'vue-property-decorator';
    import {FarmProfileAuthorize, FarmAuthorizationNonce} from '@/interfaces';
    import {dispatchAuthorizeFarm, dispatchAuthorizeNewFarm} from '@/store/farm/actions';
    import {commitRemoveFarmAuthorizationNonce, commitSetFarmAuthorizationNonce} from '@/store/main/mutations';
    import {readFarmAuthorizationNonce} from '@/store/main/getters';
    import {commitAddNotification} from '@/store/main/mutations';

    @Component
    export default class FarmAuthorizationForm extends Vue {
        @Prop({default: false}) public appName!: string;
        @Prop({default: false}) public redirectUri!: string;
        @Prop({default: null}) public apiToken!: string;
        @Prop({default: false}) public farmUrl!: string;
        @Prop({default: false}) public authCode!: string;
        @Prop({default: null}) public farmName!: string;
        @Prop({default: null}) public farmId!: number;

        // Load the the configured oauth settings for this aggregator.
        public scopes = oauthConfig.scopes!;
        public requiredScopes: string[] = oauthConfig.requiredScopes!;
        public oauthScopes: string[] = oauthConfig.defaultScopes!;

        // Generate a random string for the state param of OAuth Authorization Flow.
        public authState: string =
            Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

        // Reference to popup window.
        public windowObjectReference: any = null;

        public openSignInWindow() {
            // Save the auth state
            const nonce: FarmAuthorizationNonce = {
                apiToken: this.apiToken,
                state: this.authState,
                farmId: this.farmId,
                farmUrl: this.farmUrl,
                scopes: this.oauthScopes,
            };

            // Build the OAuth query parameters.
            const responseType = 'code';
            const clientID = oauthConfig.clientId;
            const clientSecret = oauthConfig.clientSecret;
            const scopes = this.cleanOAuthStrings();
            const redirectURI = `${apiUrl}${this.redirectUri}`;
            const state = this.authState;

            let queryParams = '';
            if (clientSecret != null) {
                queryParams = `?response_type=${responseType}&client_id=${clientID}&client_secret=${clientSecret}&scope=${scopes}&redirect_uri=${redirectURI}&state=${state}`;
            } else {
                queryParams = `?response_type=${responseType}&client_id=${clientID}&scope=${scopes}&redirect_uri=${redirectURI}&state=${state}`;
            }

            const oauthPath = '/oauth2/authorize';

            commitSetFarmAuthorizationNonce(this.$store, nonce);

            location.replace(this.farmUrl + oauthPath + queryParams);
        }

        public async finishAuthorization(authCode, authState) {
            this.$emit('update:authStarted', true);
            const nonce: FarmAuthorizationNonce | null = readFarmAuthorizationNonce(this.$store);
            if (!nonce) {
                commitAddNotification(this.$store, {
                    content: 'Authorization must be completed in the same browser session.',
                    color: 'error',
                });
                this.$router.push(this.$route.path);
                return;
            }
            this.oauthScopes = nonce.scopes!;
            const savedState = nonce.state!;
            const farmUrl = nonce.farmUrl!;
            const farmId = +nonce.farmId!;
            const apiToken = nonce.apiToken;

            if (savedState !== authState) {
                commitAddNotification(this.$store, {
                    content: 'Authorization error: State parameters do not match.',
                    color: 'error',
                });
                this.$router.push(this.$route.path);
                return;
            }

            // Remove the nonce once retrieved.
            commitRemoveFarmAuthorizationNonce(this.$store);

            // Build the payload for the backend to request a token.
            const authValues: FarmProfileAuthorize = {
                grant_type: 'authorization_code',
                code: authCode,
                state: authState,
                client_id: oauthConfig.clientId!,
                client_secret: oauthConfig.clientSecret!,
                redirect_uri: `${apiUrl}${this.redirectUri}`,
            };

            // Dispatch API call to backend.
            if (farmId !== 0 && apiToken != null) {
                await dispatchAuthorizeFarm(
                    this.$store,
                    {id: farmId, authValues, apiToken},
                ).then( (response) => {
                    this.$emit('update:authtoken', response.token);
                    this.$emit('update:apiToken', apiToken);
                    this.$emit('update:farminfo', response.info);
                    this.$emit('update:farmName', response.info.name);
                    this.$emit('update:farmUrl', response.info.url);
                    this.$emit('update:authFinished', true);
                    this.$emit('authorizationcomplete');
                });
            } else {
                await dispatchAuthorizeNewFarm(
                    this.$store,
                    {farmUrl, authValues, apiToken},
                ).then((response) => {
                    this.$emit('update:authtoken', response.token);
                    this.$emit('update:apiToken', apiToken);
                    this.$emit('update:farminfo', response.info);
                    this.$emit('update:farmName', response.info.name);
                    this.$emit('update:farmUrl', response.info.url);
                    this.$emit('update:authFinished', true);
                    this.$emit('authorizationcomplete');
                });
            }

        }

        public cleanOAuthStrings() {
                // Change the OAuth Scopes from a list of strings to one space separated string of scopes.
                // These are embedded in the query parameters.
                let allScopes: string = '';
                for (const scope of this.oauthScopes) {
                    allScopes += scope + ' ';
                }
                return allScopes;
            }

        }


</script>

<style scoped>

</style>
