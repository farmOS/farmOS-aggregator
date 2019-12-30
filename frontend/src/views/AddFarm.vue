<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm12 md8>


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
                              v-model="url"
                              v-validate="{ required: true, url: { require_protocol: true } }"
                              data-vv-name="url"
                              data-vv-scope="urlForm"
                              :error-messages="errors.first('urlForm.url')"
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
                              @click="submitForm('urlForm')"
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
                            v-bind:authstatus.sync="authStatus"
                            v-bind:authtoken.sync="authToken"
                            v-bind:farminfo.sync="farmInfo"
                            v-bind:appName="appName"
                            v-bind:farmUrl="url"
                            v-bind:farmName="farmName"
                            v-on:authorizationcomplete="nextStep(2)"
                    />
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                            color="primary"
                            @click="$refs.authForm.openSignInWindow()"
                            :disabled="authStatus == 'completed'"
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
                      />
                      <v-text-field
                              label="URL"
                              v-model="url"
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
                      <v-text-field
                              label="Tags (Optional)"
                              v-model="tags"
                              data-vv-name="tags"
                              data-vv-scope="farmInfoForm"
                              :error-messages="errors.first('farmInfoForm.tags')"
                      />
                    </form>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                            color="primary"
                            @click="submitForm('farmInfoForm')"
                    >
                      Next
                    </v-btn>
                  </v-card-actions>

                </v-card>
              </v-stepper-content>

              <!-- Step 4 - Verify and Save Farm Profile Info -->
              <v-stepper-content
                      :key="`4-content`"
                      :step="4"
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
                      />
                      <v-text-field
                              label="URL"
                              v-model="url"
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
                      <v-text-field
                              label="Tags (Optional)"
                              v-model="tags"
                              data-vv-name="tags"
                              data-vv-scope="farmInfoForm"
                              :error-messages="errors.first('farmInfoForm.tags')"
                      />
                    </form>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                            color="primary"
                            @click="submit()"
                    >
                      Save
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
import { FarmProfileCreate, FarmToken } from '@/interfaces';
import { appName, openFarmRegistration, inviteFarmRegistration } from '@/env';
import { commitAddNotification } from '@/store/main/mutations';
import { dispatchPublicCreateFarm } from '@/store/farm/actions';
import FarmAuthorizationForm from '@/components/FarmAuthorizationForm.vue';

@Component({
  components: {FarmAuthorizationForm},
})
export default class PublicAddFarm extends Vue {
  public appName = appName;
  // Query params.
  public farmID: number = 0;
  public apiToken: string = '';

  // Save the FarmProfile info.
  public farm = {} as FarmProfileCreate;

  // Initialize variables for farm profile.
  public farmName: string = '';
  public url: string = '';
  public notes: string = '';
  public tags: string = '';

  // Initialize variables for the authorization step.
  public authStatus: string = 'not started';
  public authToken: FarmToken = {
    access_token: '',
    refresh_token: '',
    expires_at: '',
    expires_in: '',
  };
  public farmInfo: object = {};


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
      header: 'Farm Info',
      complete: false,
      editable: false,
      rules: [],
    },
    {
      key: 4,
      header: 'Verify',
      complete: false,
      editable: false,
      rules: [],
    },

  ];

  public async mounted() {
    // Save an API Token if provided.
    this.apiToken = this.$router.currentRoute.query.api_token as string;

    // Check farm registration configuration.
    if (openFarmRegistration) {
      return;
    } else if (inviteFarmRegistration) {
      // Verify an APIToken was provided.
      this.checkApiToken(this.apiToken);
    } else {
      commitAddNotification(this.$store, {
        content: 'You cannot join this aggregator without an invitation from the administrator.',
        color: 'error',
      });
      this.$router.push('/');
      return;
    }

    this.reset();
  }

  public cancel() {
    this.$router.push('/');
  }

  public reset() {
    this.$validator.reset();
  }

  public submitForm(scope) {
    this.$validator.validateAll(scope).then( (isValid) => {
      if (isValid) {
          this.currentStep ++;
      }
    });
  }

  public nextStep(n) {
    this.currentStep = n + 1;
  }

  public submit() {
    const newFarm: FarmProfileCreate = {
      farm_name: this.farmName,
      url: this.url,
      tags: this.tags,
      token: this.authToken,
    };
    dispatchPublicCreateFarm(this.$store, {data: newFarm, apiToken: this.apiToken});
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
