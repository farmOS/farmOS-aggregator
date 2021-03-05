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

          <v-stepper
              v-model="currentStep"
              :vertical="false"
              :alt-labels="true"
          >

            <v-stepper-header>
              <template v-for="s in steps">
                <v-stepper-step
                    :key="`${s.key}-step`"
                    :complete="currentStep > s.key"
                    :step="s.key"
                    :editable="s.editable"
                    :rules="s.rules"
                >
                  {{ s.header }}
                </v-stepper-step>

                <v-divider
                    v-if="s !== steps"
                    :key="s.key"
                />
              </template>
            </v-stepper-header>

            <v-stepper-items>

              <!-- Step 1 - Collect farmOS Server URL -->
              <v-stepper-content
                  :key="`1-content`"
                  :step="1"
              >
                <v-card>
                  <v-card-text>
                    <template>
                      Enter the URL of your farmOS server
                    </template>
                    <form data-vv-scope="urlForm">
                      <v-text-field
                          v-model="farmInfo.url"
                          v-validate="{ required: true, url: { require_protocol: true } }"
                          data-vv-name="farmUrl"
                          data-vv-scope="urlForm"
                          :error-messages="errors.first('urlForm.farmUrl')"
                          required
                          hint="https://yourfarm.farmos.net"
                      />
                    </form>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="cancel">Cancel</v-btn>
                    <v-btn
                        color="primary"
                        @click="submitUrl"
                    >
                      Next
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-stepper-content>

              <!-- Step 2 - Authorize farmOS Server -->
              <v-stepper-content
                  :key="`2-content`"
                  :step="2"
              >
                <v-card>
                  <v-card-text>
                    <FarmAuthorizationForm
                        ref="authForm"
                        v-bind:appName="appName"
                        v-bind:redirectUri="'/authorize-farm'"
                        v-bind:apiToken.sync="apiToken"
                        v-bind:authStarted.sync="authStarted"
                        v-bind:authFinished.sync="authFinished"
                        v-bind:registerNewFarm.sync="registerNewFarm"
                        v-bind:farmId.sync="farmId"
                        v-bind:farmUrl.sync="farmInfo.url"
                        v-on:authorization-complete="handleAuthorizationComplete"
                    />
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="primary"
                        @click="$refs.authForm.openSignInWindow()"
                        :loading="authStarted === true && authFinished !== true"
                        :disabled="authStarted === true || authFinished === true"
                    >
                      Authorize
                    </v-btn>
                  </v-card-actions>

                </v-card>
              </v-stepper-content>

              <!-- Step 3 - Collect Farm Profile Info -->
              <v-stepper-content
                  :key="`3-content`"
                  :step="3"
              >
                <v-card>
                  <v-card-text>
                    <form data-vv-scope="farmInfoForm">
                      <v-text-field
                          label="Farm Name"
                          v-model="farmInfo.name"
                          v-validate="'required'"
                          data-vv-name="name"
                          data-vv-scope="farmInfoForm"
                          :error-messages="errors.first('farmInfoForm.name')"
                          required
                          readonly
                      />
                      <v-text-field
                          label="URL"
                          v-model="farmInfo.url"
                          v-validate="{ required: true, url: {require_protocol: true } }"
                          data-vv-name="url"
                          data-vv-scope="farmInfoForm"
                          :error-messages="errors.first('farmInfoForm.url')"
                          required
                          readonly
                      />
                      <v-text-field
                          label="API Version"
                          v-model="farmInfo.api_version"
                          data-vv-name="api_version"
                          data-vv-scope="farmInfoForm"
                          :error-messages="errors.first('farmInfoForm.api_version')"
                          required
                          readonly
                      />
                    </form>
                  </v-card-text>

                  <!--Text for successful registration.-->
                  <v-card-text
                      v-if="registerSuccess"
                  >
                    <p>
                      Your farm, <strong>{{ farmInfo.name }}</strong>, was successfully registered with the {{ appName }}!
                    </p>

                    <p class="font-weight-black">
                      Your farm has ID={{ farmId }}
                    </p>

                    <p>
                      No further action is required. You may close this window.
                    </p>

                    <p>
                      Administrators of the {{ appName }} must approve your farm before its data will be used.
                    </p>
                  </v-card-text>

                  <!--Text for successful re-authorization.-->
                  <v-card-text
                      v-if="reauthorizeSuccess"
                  >
                    <p>
                      Your farm, <strong>{{ farmInfo.name }}</strong>, was successfully re-authorized with the {{ appName }}!
                    </p>

                    <p class="font-weight-black">
                      Your farm has ID={{ farmId }}
                    </p>

                    <p>
                      No further action is required. You may close this window.
                    </p>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="primary"
                        v-if="registerNewFarm"
                        :disabled="registerComplete"
                        @click="createFarm"
                    >
                      Register
                    </v-btn>
                  </v-card-actions>

                </v-card>

              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>

        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {FarmInfo, FarmProfile, FarmProfileCreate, FarmToken} from '@/interfaces';
import { env } from '@/env';
import { commitAddNotification } from '@/store/main/mutations';
import {dispatchCreateFarm, dispatchGetOneFarm, dispatchValidateFarmUrl} from '@/store/farm/actions';
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
  public openFarmRegistration = env('openFarmRegistration');
  public inviteFarmRegistration = env('inviteFarmRegistration');

  // Query params.
  public farmId: number = 0;
  public apiToken: string = '';

  // Initialize form variables.
  public tags: string = '';
  public scope: string = '';

  // Initialize variables for farm profile.
  public farmInfo: FarmInfo = {
    name: '',
    url: '',
    api_version: '',
  };
  // Initialize variables for the authorization step.
  public authStarted: boolean = false;
  public authFinished: boolean = false;
  public registerNewFarm: boolean = false;
  public registerComplete: boolean = false;
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

  // Variables for success dialog
  public registerSuccess: boolean = false;
  public reauthorizeSuccess: boolean = false;

  public currentStep: number = 1;
  public steps: object[] = [
    {
      key: 1,
      header: 'farmOS URL',
      complete: false,
      editable: false,
      rules: [],
    },
    {
      key: 2,
      header: 'Authorize',
      complete: false,
      editable: false,
      rules: [],
    },
    {
      key: 3,
      header: 'Verify',
      complete: false,
      editable: false,
      rules: [],
    },

  ];

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
          this.currentStep = 2;
          // Finish authorization in the FarmAuthorizationFrom component.
          this.$refs.authForm.finishAuthorization(this.authCode, this.authState);
          return;
      }

      // Save an API Token if provided.
      this.farmId = +this.$router.currentRoute.query.farm_id as number;
      this.apiToken = this.$router.currentRoute.query.api_token as string;

      // If no farm ID is populated, see if we can register a new farm.
      if (!this.farmId) {

        // Check farm registration configuration.
        if (!this.openFarmRegistration && this.inviteFarmRegistration) {
          // Verify an APIToken was provided.
          if (!this.apiToken) {
            commitAddNotification(this.$store, {
              content: 'You cannot register farms without an invitation from the administrator.',
              color: 'error',
            });
            this.$router.push('/');
          }
        }

        if (!this.openFarmRegistration && !this.inviteFarmRegistration) {
          commitAddNotification(this.$store, {
            content: 'You cannot join this aggregator without an invitation from the administrator.',
            color: 'error',
          });
          this.$router.push('/');
          return;
        }
      } else {
        // Authorization is starting from a link with ID and api_token provided.

        if (!this.apiToken) {
          commitAddNotification(this.$store, {
            content: 'You cannot re-authorize farms without an invitation from the administrator.',
            color: 'error',
          });
          this.$router.push('/');
          return;
        }

        // Verify a valid api_token was provided and load farm info.
        const response = await dispatchGetOneFarm(this.$store, { farmID: this.farmId, apiToken: this.apiToken } );
        if (response) {
          this.farmInfo = {
            name: response.farm_name,
            url: response.url,
            api_version: '',
          };
        } else {
          commitAddNotification(this.$store, {
            content: 'Farm not found, cannot authorize.',
            color: 'error',
          });
          this.$router.push('/');
          return;
        }

        this.currentStep = 2;
      }
      this.reset();
  }

  public reset() {
    this.$validator.reset();
  }

  public cancel() {
    this.$router.push('/');
  }

  public async submitUrl() {
    this.$validator.validateAll('farmUrl').then( (isValid) => {
      if (isValid) {
        dispatchValidateFarmUrl(
            this.$store,
            {farmUrl: this.farmInfo.url, apiToken: this.apiToken },
        ).then( (response) => {

          // Check if the farm exists.
          if (response.id === null) {
            this.registerNewFarm = true;
          } else {
            this.farmId = response.id;
          }

          this.apiToken = response.api_token;
          this.currentStep = 2;
        });
      }
    });
  }

  public handleAuthorizationComplete(response) {
    this.authToken = response.token;
    this.farmInfo = {
      name: response.info.name,
      url: response.info.url,
      api_version: response.info.api_version ? response.info.api_version : response.info.version,
    };
    this.currentStep = 3;

    // Display a re-authorize success message.
    if (!this.registerNewFarm) {
      this.reauthorizeSuccess = true;
    }
  }

  public createFarm() {
    this.registerComplete = true;
    this.$validator.validateAll('FarmVerifyForm').then((isValid) => {
      if (isValid && !!this.farmInfo) {
        const newFarm: FarmProfileCreate = {
          farm_name: this.farmInfo.name,
          url: this.farmInfo!.url,
          tags: '',
          token: this.authToken,
          scope: this.scope,
        };
        dispatchCreateFarm(
            this.$store,
            {data: newFarm, apiToken: this.apiToken},
        ).then((response) => {
              this.registerSuccess = true;
              this.farmId = response.id;
            },
        );
      }
    });
  }
}
</script>
