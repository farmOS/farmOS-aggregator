<template>
  <v-container fluid>
    <v-card class="ma-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Authorize Farm</div>
      </v-card-title>

      <v-card-title class="headline">
        Farm Info
      </v-card-title>

      <v-card-text>
        <v-text-field label="Farm Name" v-model="farmName" readonly></v-text-field>
        <v-text-field label="URL" v-model="url" readonly></v-text-field>

      </v-card-text>

      <v-card-title>
          OAuth Token
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
      </v-card-title>
        <v-card-text>
            <v-text-field  :disabled="!hasToken" label="Access Token" v-model="accessToken" readonly ></v-text-field>
            <v-text-field  :disabled="!hasToken" label="Expires In" v-model="expiresIn" readonly ></v-text-field>
            <v-text-field  :disabled="!hasToken" label="Expires At" v-model="expiresAt" readonly ></v-text-field>
            <v-text-field  :disabled="!hasToken" label="Refresh Token" v-model="refreshToken" readonly ></v-text-field>

        </v-card-text>

        <v-card-actions>
         <v-spacer></v-spacer>
         <v-btn @click="cancel">Cancel</v-btn>
         <v-btn
                 color="secondary"
                 @click.stop="authorizationDialog = true"

         >
             Request Authorization
         </v-btn>

        <v-btn
                class="white--text"
                color="primary"
                @click="openSignInWindow"
        >
            Authorize Now
        </v-btn>

        <v-dialog
                v-model="authorizationDialog"
                max-width="300"
        >
            <v-card>
                <v-card-title class="headline">Request Authorization</v-card-title>

                <v-card-text>
                    Select an email to send the Authorization Request to.
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                            color="green darken-1"
                            text
                            @click="dialog = false"
                    >
                        Cancel
                    </v-btn>

                    <v-btn
                            color="green darken-1"
                            text
                            @click="dialog = false"
                    >
                        Send
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
     </v-card-actions>

    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { FarmProfileAuthorize } from '@/interfaces';
import { dispatchGetFarms, dispatchAuthorizeFarm} from '@/store/farm/actions';
import { readOneFarm } from '@/store/farm/getters';

@Component
export default class EditFarm extends Vue {
  public valid = false;
  public authorizationDialog = false;
  public farmName: string = '';
  public url: string = '';
  public username: string = '';
  public notes: string = '';
  public tags: string = '';
  public isAuthorized = false;
  public hasToken = false;
  public accessToken: string = '';
  public refreshToken: string = '';
  public expiresIn: string = '';
  public expiresAt: string = '';

  public windowObjectReference: any = null;

  public async mounted() {
    await dispatchGetFarms(this.$store);
    this.reset();
  }

  public reset() {
    this.hasToken = false;
    this.$validator.reset();
    if (this.farm) {
      this.farmName = this.farm.farm_name;
      this.url = this.farm.url;
      this.username = this.farm.username;
      this.notes = this.farm.notes!;
      this.tags = this.farm.tags!;
      this.isAuthorized = this.farm.is_authorized;

      if (this.farm.token) {
        this.hasToken = true;
        this.accessToken = this.farm.token.access_token;
        this.refreshToken = this.farm.token.refresh_token;
        this.expiresIn = this.farm.token.expires_in;
        this.expiresAt = this.farm.token.expires_at;
      }
    }
  }

  public cancel() {
    this.$router.back();
  }

  public openSignInWindow() {
      const windowFeatures = 'toolbar=no, menubar=no, width=600, height=700, top=100, left=100';

      const oauthPath = '/oauth2/authorize';
      const queryParams = '?response_type=code&client_id=farmos_api_client&redirect_uri=http://192.168.1.9/api/authorized&state=p4W8P5f7gJCIDbC1Mv78zHhlpJOidy';

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
      console.log(event);

      // Build a URLSearchParams from the message data.
      const params = new URLSearchParams(event.data.substr(1));

      // Parse out the `code` and `state` values.
      const code = params.get('code') as string;
      const state = params.get('state') as string;

      // Build the payload for the backend to request a token.
      const authValues: FarmProfileAuthorize = {
          grant_type: 'authorization_code',
          code,
          state,
          client_id: 'farmos_api_client',
          client_secret: 'client_secret',
      };

      // Dispatch API call to backend.
      dispatchAuthorizeFarm(this.$store, { id: this.farm!.id, authValues });
      // this.$router.push('/main/farm/farms/authorize/' + this.farm!.id);
  }

  get farm() {
    return readOneFarm(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
