<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Add a Farm</div>
      </v-card-title>

      <v-form v-model="valid" ref="form" lazy-validation>
        <v-card-text>
          <v-text-field label="Farm Name" v-model="farmName" required></v-text-field>
          <v-text-field label="URL" v-model="url" required></v-text-field>
          <v-text-field label="Notes (Optional)" v-model="notes"></v-text-field>
          <v-text-field label="Tags (Optional)" v-model="tags"></v-text-field>


          <div class="d-flex">
            <v-checkbox
                    v-model="includeCredentials"
                    label="Include farmOS user credentials"
            ></v-checkbox>
          </div>

          <v-expansion-panels
                  multiple
                  accordion
          >
            <v-expansion-panel
                    :disabled="!includeCredentials"
            >
              <v-expansion-panel-header>
                farmOS Credentials
              </v-expansion-panel-header>
              <v-expansion-panel-content>

                <v-text-field
                        label="Username"
                        v-model="username"
                        :disabled="!includeCredentials"
                >
                </v-text-field>

                <v-text-field
                        type="password"
                        ref="password"
                        label="Set Password"
                        data-vv-name="password"
                        data-vv-delay="100"
                        v-model="password1"
                        :disabled="!includeCredentials"
                        :error-messages="errors.first('password')"
                >
                </v-text-field>
                <v-text-field
                        type="password"
                        label="Confirm Password"
                        data-vv-name="password_confirmation"
                        data-vv-delay="100"
                        data-vv-as="password"
                        v-validate="{confirmed: 'password'}"
                        v-model="password2"
                        :disabled="!includeCredentials"
                        :error-messages="errors.first('password_confirmation')"
                >
                </v-text-field>

              </v-expansion-panel-content>
            </v-expansion-panel>

          </v-expansion-panels>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="cancel">Cancel</v-btn>
          <v-btn @click="reset">Reset</v-btn>
          <v-btn
                  @click="submit"
                  :disabled="!valid"
          >
            Save
          </v-btn>
        </v-card-actions>


      </v-form>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  FarmProfileCreate,
} from '@/interfaces';
import { dispatchGetFarms, dispatchCreateFarm } from '@/store/farm/actions';

@Component
export default class AddFarm extends Vue {
  public valid = false;
  public farmName: string = '';
  public url: string = '';
  public username: string = '';
  public password1: string = '';
  public password2: string = '';
  public notes: string = '';
  public tags: string = '';
  public includeCredentials = false;


  public async mounted() {
    await dispatchGetFarms(this.$store);
    this.reset();
  }

  public reset() {
    this.includeCredentials = false;
    this.password1 = '';
    this.password2 = '';
    this.farmName = '';
    this.username = '';
    this.notes = '';
    this.tags = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedFarm: FarmProfileCreate = {
        farm_name: this.farmName,
        url: this.url,
        username: this.username,
        password: this.password1,
        notes: this.notes,
        tags: this.tags,
      };
      await dispatchCreateFarm(this.$store, updatedFarm);
      this.$router.push('/main/farm/farms');
    }
  }
}
</script>
