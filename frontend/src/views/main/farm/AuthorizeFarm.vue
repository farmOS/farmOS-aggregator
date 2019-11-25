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
        <v-text-field label="User Email" v-model="userEmail" :loading="farmInfoLoading" readonly></v-text-field>

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

        <v-dialog
                v-model="authorizationDialog"
                max-width="600"
        >
            <v-card>
                <v-card-title class="headline">Request Authorization</v-card-title>

                <v-card-text>
                    Input the email to send a verification link. By default, this is the farmOS admin email.

                    <v-text-field type="email" label="farmOS Admin Email" v-model="userEmail"></v-text-field>

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
                            @click="authorizationDialog = false"
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
import { dispatchGetFarms, dispatchAuthorizeFarm, dispatchCreateFarmAuthLink, dispatchGetFarmInfo } from '@/store/farm/actions';
import { readOneFarm } from '@/store/farm/getters';

@Component
export default class EditFarm extends Vue {
  // Properties from the Farm Profile.
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

  // Properties from the farmOS server, retrieved via API.
  public farmInfoLoading: boolean = false;
  public userEmail: string = 'Loading...';

  // Properties for the Authorization Diaglog.
  public authorizationDialog = false;
  public authLinkLoading: boolean = false;
  public authLinkLoaded: boolean = false;
  public authLink: string = '';

  public async mounted() {
    await dispatchGetFarms(this.$store);
    this.reset();
    if (this.farm) {
        this.farmInfoLoading = true;
        await dispatchGetFarmInfo(this.$store, { farmID: this.farm.id }).then(this.setFarmInfo);
        this.farmInfoLoading = false;
    }
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

  public setFarmInfo(farmInfo) {
    // Save farm info retrieved via API in the Vue state.
    if (farmInfo.info) {
        this.userEmail = farmInfo.info.user.mail;
    } else {
        this.userEmail = 'No email found.';
    }
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
