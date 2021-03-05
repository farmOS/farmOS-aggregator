<template>
  <div>
    <form>
      <div class="headline text--primary">
        farmOS Server Authorization
      </div>
      <div class="subtitle-1 text--primary">
        Authorize your farmOS server with the {{appName}}. This will give the {{appName}} access to your data
        at the level you define.
      </div>
      <br>
      <v-text-field label="farmOS Server URL" v-model="farmUrl" prefix="https://" readonly></v-text-field>


      <div class="headline text--primary">
        Permissions
      </div>
      <v-checkbox
        v-for="scope in oauthScopes"
        v-model="oauthSelectedScopes"
        v-bind:key="scope.name"
        v-bind:value="scope.name"
        v-bind:label="scope.label"
        v-bind:hint="scope.description"
        :disabled = "oauthRequiredScopes.includes(scope.name)"
        persistent-hint
      ></v-checkbox>
    </form>
  </div>
</template>

<script lang="ts">
    import { env } from '@/env';
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
        @Prop({default: false}) public registerNewFarm!: boolean;
        @Prop({default: null}) public apiToken!: string;
        @Prop({default: false}) public farmUrl!: string;
        @Prop({default: null}) public farmId!: number;

        // Load environment config
        public apiUrl = env('apiUrl');

        // Variables.
        public authCode: string = '';

        // Load the the configured oauth settings for this aggregator.
        public oauthClientId = env('oauthClientId');
        public oauthClientSecret = env('oauthClientSecret');
        public oauthScopes = env('oauthScopes');
        public oauthRequiredScopes = env('oauthRequiredScopes');

        // Selected Scopes starts as Default OAuth Scopes
        public oauthSelectedScopes = env('oauthDefaultScopes');

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
                registerNewFarm: this.registerNewFarm,
                farmId: this.farmId,
                farmUrl: this.farmUrl,
                scopes: this.oauthSelectedScopes,
            };

            // Build the OAuth query parameters.
            const responseType = 'code';
            const clientID = this.oauthClientId;
            const clientSecret = this.oauthClientSecret;
            const scopes = this.cleanOAuthStrings();
            const redirectURI = `${this.apiUrl}${this.redirectUri}`;
            const state = this.authState;

            let queryParams = '';
            if (clientSecret != null) {
                queryParams = `?response_type=${responseType}&client_id=${clientID}&client_secret=${clientSecret}&scope=${scopes}&redirect_uri=${redirectURI}&state=${state}`;
            } else {
                queryParams = `?response_type=${responseType}&client_id=${clientID}&scope=${scopes}&redirect_uri=${redirectURI}&state=${state}`;
            }

            const oauthPath = '/oauth/authorize';

            commitSetFarmAuthorizationNonce(this.$store, nonce);

            const url = 'http://' + this.farmUrl.replace(/(^\w+:|^)\/\//, '');

            location.replace(url + oauthPath + queryParams);
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
            this.oauthSelectedScopes = nonce.scopes!;
            const scope = this.cleanOAuthStrings();
            const savedState = nonce.state!;
            this.$emit('update:registerNewFarm', nonce.registerNewFarm!);
            const farmUrl = nonce.farmUrl!;
            this.$emit('update:farmUrl', farmUrl);
            const farmId = +nonce.farmId!;
            this.$emit('update:farmId', farmId);
            const apiToken = nonce.apiToken;
            this.$emit('update:apiToken', apiToken);

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
                client_id: this.oauthClientId,
                client_secret: this.oauthClientSecret,
                redirect_uri: `${this.apiUrl}${this.redirectUri}`,
                scope,
            };

            // Dispatch API call to backend.
            if (farmId !== 0 && apiToken != null) {
                await dispatchAuthorizeFarm(
                    this.$store,
                    {id: farmId, authValues, apiToken},
                ).then( (response) => {
                  this.$emit('update:apiToken', apiToken);
                  this.$emit('update:authFinished', true);
                  this.$emit('authorization-complete', response);
                });
            } else {
                await dispatchAuthorizeNewFarm(
                    this.$store,
                    {farmUrl, authValues, apiToken},
                ).then((response) => {
                  this.$emit('update:apiToken', apiToken);
                  this.$emit('update:authFinished', true);
                  this.$emit('authorization-complete', response);
                });
            }

        }

        public cleanOAuthStrings() {
                // Change the OAuth Scopes from a list of strings to one space separated string of scopes.
                // These are embedded in the query parameters.
                let allScopes: string = '';
                for (const scope of this.oauthSelectedScopes) {
                    allScopes += scope + ' ';
                }
                return allScopes;
            }

        }


</script>

<style scoped>

</style>
