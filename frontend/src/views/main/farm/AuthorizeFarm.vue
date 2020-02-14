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
        <v-text-field label="OAuth Scope" v-model="scope" readonly></v-text-field>
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
                 color="primary"
                 @click="$refs.AuthorizationRegistrationDialog.openDialog()"

         >
             Request Authorization
         </v-btn>

          <FarmAuthorizationRegistrationDialog
            ref="AuthorizationRegistrationDialog"
            v-bind:farmID="farmId"

          />
     </v-card-actions>

    </v-card>
  </v-container>
</template>

<script lang="ts">
import { env } from '@/env';
import { Component, Vue } from 'vue-property-decorator';
import { dispatchGetFarms, dispatchCreateFarmAuthLink, dispatchGetFarmInfo } from '@/store/farm/actions';
import { readOneFarm } from '@/store/farm/getters';
import FarmAuthorizationStatus from '@/components/FarmAuthorizationStatus.vue';
import FarmAuthorizationForm from '@/components/FarmAuthorizationForm.vue';
import FarmAuthorizationRegistrationDialog from '@/components/FarmAuthorizationRegistrationDialog.vue';

@Component({
    components: {FarmAuthorizationRegistrationDialog, FarmAuthorizationStatus, FarmAuthorizationForm},
})
export default class AuthorizeFarm extends Vue {
  public appName = env('appName');

  // Properties from the Farm Profile.
  public farmName: string = '';
  public farmId: number = 0;
  public url: string = '';
  public scope: string = '';
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
      this.scope = this.farm.scope!;
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

  get farm() {
    return readOneFarm(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
