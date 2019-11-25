<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="ma-3">
            <v-toolbar dark color="primary">
              <v-toolbar-title class="headline">Authorize farmOS</v-toolbar-title>
            </v-toolbar>

            <v-card-text>
              <div class="subtitle-1 text--primary">
                Authorize your farmOS server with the {{appName}}. This will give the {{appName}} access to your data
                at the level you define.
              </div>
              <br>
              <div class="headline text--primary">
                Farm Info
                <v-chip
                        v-if="isAuthorized"
                        depressed
                        small
                        color="success"
                        class="ma-3"
                >
                  Authorized
                </v-chip>
                <v-chip
                        v-else
                        depressed
                        small
                        color="error"
                        class="ma-3"
                >
                  Not Authorized
                </v-chip>
              </div>
              <div class="text--primary">
                Verify that the following information is correct:
              </div>
              <v-text-field label="Farm Name" v-model="farmName" readonly></v-text-field>
              <v-text-field label="URL" v-model="url" readonly></v-text-field>


              <div class="headline text--primary">
                Permissions
              </div>
              <v-checkbox
                      v-model="oauthScopes"
                      label="farmOS API Access"
                      hint="Allow access to the entire farmOS API"
                      value="farmos_restws_access"
                      persistent-hint
                      disabled
              ></v-checkbox>
              <br>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="cancel">Cancel</v-btn>

              <v-btn
                      class="white--text"
                      color="primary"
                      @click="openSignInWindow"
              >
                Authorize Now
              </v-btn>

            </v-card-actions>

          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { FarmProfile, FarmProfileAuthorize } from '@/interfaces';
import { appName } from '@/env';
import { commitAddNotification } from '@/store/main/mutations';
import { dispatchGetOneFarm, dispatchAuthorizeFarm } from '@/store/farm/actions';

@Component
export default class UserProfileEdit extends Vue {
  public appName = appName;
  // Query params.
  public farmID: number = 0;
  public apiToken: string = '';

  // Save the FarmProfile info.
  public farm = {} as FarmProfile;
  public farmName: string = '';
  public url: string = '';
  public isAuthorized: boolean = false;

  // Enable the farmos_restws_access scope by default.
  public oauthScopes: string[] = ['farmos_restws_access'];

  // Generate a random string for the state param of OAuth Authorization Flow.
  public authState: string = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);


  // Reference to popup window.
  public windowObjectReference: any = null;

  public async mounted() {
    this.farmID = +this.$router.currentRoute.params.id;
    this.apiToken = this.$router.currentRoute.query.api_token as string;

    // Verify an APIToken was provided.
    this.checkApiToken(this.apiToken);
    const response = await dispatchGetOneFarm(this.$store, { farmID: this.farmID, apiToken: this.apiToken } );
    if (response) {
      this.farm = response;
    }

    this.reset();

  }

  public reset() {
    this.$validator.reset();
    if (this.farm) {
      this.farmName = this.farm.farm_name;
      this.url = this.farm.url;
      this.isAuthorized = this.farm.is_authorized;
    }
  }

  public cancel() {
    this.$router.push('/');
  }

  public checkApiToken(token) {
    // Make sure a Token was included as an api_token query parameter.
    if (!token) {
      commitAddNotification(this.$store, {
        content: 'No token provided in the URL, start a new password recovery',
        color: 'error',
      });
      this.$router.push('/recover-password');
    } else {
      return token;
    }
  }

  public openSignInWindow() {
    const windowFeatures = 'toolbar=no, menubar=no, width=600, height=700, top=100, left=100';

    // Build the OAuth query parameters.
    const responseType = 'code';
    const clientID = 'farmos_api_client';
    const scopes = this.cleanOAuthStrings();
    const redirectURI = `${this.farm.url}/api/authorized`;
    const state = this.authState;
    const queryParams = `?response_type=${responseType}&client_id=${clientID}&scope=${scopes}&redirect_uri=${redirectURI}&state=${state}`;

    const oauthPath = '/oauth2/authorize';

    // Open a pop up window with the OAuth Authorization URL.
    if (this.windowObjectReference === null || this.windowObjectReference.closed) {
      this.windowObjectReference = window.open(this.url + oauthPath + queryParams, 'farmOS Login', windowFeatures);
      this.windowObjectReference.focus();
    } else {
      this.windowObjectReference.focus();
    }

    // Add listener to retrieve the OAuth Code
    window.addEventListener('message', (event) => this.receiveMessage(event), false);
  }

  public async receiveMessage(event) {
    // Make sure the message came from the farmOS server.
    if (event.origin !== this.url) {
      return;
    }

    // Build a URLSearchParams from the message data.
    const params = new URLSearchParams(event.data.substr(1));

    // Parse out the `code` and `state` values.
    const code = params.get('code') as string;
    const state = params.get('state') as string;

    // Make sure the state did not change.
    if (state !== this.authState) {
      return null;
    }

    // Build the payload for the backend to request a token.
    const authValues: FarmProfileAuthorize = {
      grant_type: 'authorization_code',
      code,
      state,
      client_id: 'farmos_api_client',
      client_secret: 'client_secret',
    };

    // Dispatch API call to backend.
    await dispatchAuthorizeFarm(this.$store, { id: this.farm!.id, authValues, apiToken: this.apiToken });
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
