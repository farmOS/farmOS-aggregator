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
        <v-text-field v-if="hasError" label="Authentication Error" v-model="authError" readonly/>

        <FarmAuthorizationStatus v-bind:farm=farm></FarmAuthorizationStatus>

      </v-card-text>

      <v-card-title>
          OAuth Token
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
                 @click="authorizeNow(farm.id)"
                 :loading="authLinkLoading"
                 :disabled="authLinkLoading"
         >
             Authorize Now
         </v-btn>
         <v-btn
                 color="primary"
                 @click.stop="authorizationRequestDialog = true"

         >
             Request Authorization
         </v-btn>

        <v-dialog
                v-model="authorizationRequestDialog"
                max-width="600"
        >
            <v-card>
                <v-card-title class="headline">Request Authorization</v-card-title>

                <v-card-text>
                    Input the email to send a verification link. By default, this is the farmOS admin email.

                    <v-text-field type="email" label="farmOS Admin Email" ></v-text-field>

                    OR

                    <v-btn
                            class="ma-2"
                            :loading="authLinkLoading"
                            :disabled="authLinkLoaded"
                            color="secondary"
                            @click="generateAuthLink(farm.id)"
                    >
                        Generate Authorization Link
                    </v-btn>

                    <v-text-field
                            label="Authorization Link"
                            v-if="authLinkLoaded"
                            v-model="authLink"
                            readonly
                    ></v-text-field>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                            color="green darken-1"
                            text
                            @click="authorizationRequestDialog = false"
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
import { appName } from '@/env';
import { Component, Vue } from 'vue-property-decorator';
import { dispatchGetFarms, dispatchCreateFarmAuthLink, dispatchGetFarmInfo } from '@/store/farm/actions';
import { readOneFarm } from '@/store/farm/getters';
import FarmAuthorizationStatus from '@/components/FarmAuthorizationStatus.vue';
import FarmAuthorizationForm from '@/components/FarmAuthorizationForm.vue';
import {FarmProfile} from '@/interfaces';

@Component({
    components: {FarmAuthorizationStatus, FarmAuthorizationForm},
})
export default class AuthorizeFarm extends Vue {
  public appName = appName;

  // Properties from the Farm Profile.
  public farmName: string = '';
  public farmId: number = 0;
  public url: string = '';
  public notes: string = '';
  public tags: string = '';
  public isAuthorized = false;
  public authError?: string;
  public hasError: boolean = false;
  public hasToken = false;
  public accessToken: string = '';
  public refreshToken: string = '';
  public expiresIn: string = '';
  public expiresAt: string = '';

  // Properties for the Authorization Form Dialog.
  public authorizationFormDialog = false;
  public authStatus = 'not started';

  // Properties for the Authorization Request Dialog.
  public authorizationRequestDialog = false;
  public authLinkLoading: boolean = false;
  public authLinkLoaded: boolean = false;
  public authLink: string = '';

  public async mounted() {
    await dispatchGetFarms(this.$store);
    this.reset();
  }

  public reset() {
    this.hasToken = false;
    this.$validator.reset();
    if (this.farm) {
      this.farmName = this.farm.farm_name;
      this.farmId = this.farm.id;
      this.url = this.farm.url;
      this.notes = this.farm.notes!;
      this.tags = this.farm.tags!;
      this.isAuthorized = this.farm.is_authorized;

      if (this.farm.auth_error) {
          this.hasError = true;
          this.authError = this.farm.auth_error!;
      }

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

  public async authorizeNow(farmID) {
      await this.generateAuthLink(farmID).then( (res) => {
          // Redirect to the authorization page.
          location.replace(this.authLink);
      });
  }

  public async generateAuthLink(farmID) {
      // Query the API to get an Authorization link with an API token embedded in the query params.
      this.authLinkLoading = true;
      const link = await dispatchCreateFarmAuthLink(this.$store, { farmID });
      if (link) {
          this.authLink = link;
          this.authLinkLoaded = true;
      }
      this.authLinkLoading = false;
  }

  get farm() {
    return readOneFarm(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
