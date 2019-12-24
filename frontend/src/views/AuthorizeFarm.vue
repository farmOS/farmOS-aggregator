<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="">
            <v-toolbar dark color="primary">
              <v-toolbar-title class="headline">Authorize farmOS</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <FarmAuthorizationForm
                      ref="authForm"
                      v-bind:authstatus.sync="authStatus"
                      v-bind:appName="appName"
                      v-bind:farmUrl="farm.url"
                      v-bind:farmName="farm.farm_name"
                      v-bind:farmId="farm.id"
                      v-bind:apiToken="apiToken"
              />
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                      @click="$router.back()"
              >
                Cancel
              </v-btn>

              <v-btn
                      class="white--text"
                      color="primary"
                      @click="$refs.authForm.openSignInWindow()"
                      :disabled="authStatus == 'completed'"
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
import { FarmProfile } from '@/interfaces';
import { appName } from '@/env';
import { commitAddNotification } from '@/store/main/mutations';
import { dispatchGetOneFarm } from '@/store/farm/actions';
import FarmAuthorizationForm from '@/components/FarmAuthorizationForm.vue';

@Component({
  components: {FarmAuthorizationForm},
})
export default class UserProfileEdit extends Vue {
  public appName = appName;
  // Query params.
  public farmID: number = 0;
  public apiToken: string = '';

  // Save the FarmProfile info.
  public farm = {} as FarmProfile;

  public authStatus: string = 'not started';

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
}
</script>
