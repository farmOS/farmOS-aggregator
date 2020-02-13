<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>

          <v-dialog
            v-model="authErrorDialog"
            max-width="500"
          >
            <v-card color="#EF9A9A">
              <v-card-title class="headline ">Authorization Error</v-card-title>

              <v-card-text>
                <div class="title">
                  {{ authErrorDialogText }}
                </div>
                <div class="body-1">
                  {{ authErrorDialogDescriptionText }}
                </div>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                  color="white"
                  text
                  @click="authErrorDialog = false"
                >
                  Try Again
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-card class="">
            <v-toolbar dark color="primary">
              <v-toolbar-title class="headline">Authorize farmOS</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <FarmAuthorizationForm
                      ref="authForm"
                      v-bind:authStarted.sync="authStarted"
                      v-bind:authFinished.sync="authFinished"
                      v-bind:appName="appName"
                      v-bind:redirectUri="'/authorize-farm'"
                      v-bind:apiToken="apiToken"
                      v-bind:farmUrl.sync="farm.url"
                      v-bind:farmId="farm.id"
              />
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                      class="white--text"
                      color="primary"
                      @click="$refs.authForm.openSignInWindow()"
                      :loading="authStarted === true && authFinished !== true"
                      :disabled="authStarted === true || authFinished === true"
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
import {FarmProfile, FarmToken} from '@/interfaces';
import { env } from '@/env';
import { commitAddNotification } from '@/store/main/mutations';
import { dispatchGetOneFarm } from '@/store/farm/actions';
import FarmAuthorizationForm from '@/components/FarmAuthorizationForm.vue';

@Component({
  components: {FarmAuthorizationForm},
})
export default class UserProfileEdit extends Vue {
  public $refs!: {
      authForm: HTMLFormElement,
  };

  // Load environment configs
  public appName = env('appName');

  // Query params.
  public farmID: number = 0;
  public apiToken: string = '';

  // Save the FarmProfile info.
  public farm = {} as FarmProfile;

  // Initialize variables for the authorization step.
  public authStarted: boolean = false;
  public authFinished: boolean = false;
  public authCode: string = '';
  public authState: string = '';
  public authError: string = '';
  public authErrorDialog: boolean = false;
  public authErrorDialogText: string = '';
  public authErrorDialogDescriptionText: string = '';
  public authErrorDescription: string = '';
  public authToken: FarmToken = {
      access_token: '',
      refresh_token: '',
      expires_at: '',
      expires_in: '',
  };

  public async mounted() {
      // Check for authorization errors.
      this.authError = this.$router.currentRoute.query.error as string;
      this.authErrorDescription = this.$router.currentRoute.query.error_description as string;
      if (this.authError) {
          if (this.authError === 'invalid_scope') {
              this.authErrorDialogText = 'OAuth Scope Error';
              this.authErrorDialogDescriptionText = 'Your farmOS server does not have an Authorization Scope enabled. Ensure this is enabled in /admin/config/farm/oauth ';
              this.authErrorDialog = true;

          } else if (this.authError === 'access_denied') {
              this.authErrorDialogText = 'Authorization Denied';
              this.authErrorDialogDescriptionText = 'You denied the Authorization request. In order to add your farm to the ' + this.appName + ', you must authorize access to your farmOS Server.';
              this.authErrorDialog = true;
          } else {
              commitAddNotification(this.$store, {
                  content: this.authError + ': ' + this.authErrorDescription,
                  color: 'error',
              });
          }
          return;
      }

      // Get authorization code and authorization state
      this.authCode = this.$router.currentRoute.query.code as string;
      this.authState = this.$router.currentRoute.query.state as string;
      if (this.authCode && this.authState) {
          // Finish authorization in the FarmAuthorizationFrom component.
          this.$refs.authForm.finishAuthorization(this.authCode, this.authState);
          return;
      }

      // Save an API Token if provided.
      this.farmID = +this.$router.currentRoute.query.farm_id as number;
      this.apiToken = this.$router.currentRoute.query.api_token as string;

      if (!this.farmID || !this.apiToken) {
          commitAddNotification(this.$store, {
              content: 'You cannot re-authorize farms without an invitation from the administrator.',
              color: 'error',
          });
          this.$router.push('/');
          return;
      }

      // Verify an APIToken was provided.
      const response = await dispatchGetOneFarm(this.$store, { farmID: this.farmID, apiToken: this.apiToken } );
      if (response) {
          this.farm = response;
      } else {
          commitAddNotification(this.$store, {
              content: 'Farm not found, cannot authorize.',
              color: 'error',
          });
          this.$router.push('/');
          return;
      }

      this.reset();
  }

  public reset() {
    this.$validator.reset();
 }

  public cancel() {
    this.$router.push('/');
  }
}
</script>
