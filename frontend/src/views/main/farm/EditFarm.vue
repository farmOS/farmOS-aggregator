<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Farm</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Farm Name" v-model="farm_name" required></v-text-field>
            <v-text-field label="url" v-model="url" required></v-text-field>
            <v-text-field label="username" v-model="username" required></v-text-field>

            <v-layout align-center>
              <v-flex shrink>
                <v-checkbox
                  v-model="setPassword"
                  class="mr-2"
                ></v-checkbox>
              </v-flex>
              <v-flex>
                <v-text-field
                  :disabled="!setPassword"
                  type="password"
                  ref="password"
                  label="Set Password"
                  data-vv-name="password"
                  data-vv-delay="100"
                  v-validate="{required: setPassword}"
                  v-model="password1"
                  :error-messages="errors.first('password')"
                >
                </v-text-field>
                <v-text-field
                  v-show="setPassword"
                  type="password"
                  label="Confirm Password"
                  data-vv-name="password_confirmation"
                  data-vv-delay="100"
                  data-vv-as="password"
                  v-validate="{required: setPassword, confirmed: 'password'}"
                  v-model="password2"
                  :error-messages="errors.first('password_confirmation')"
                >
                </v-text-field>
              </v-flex>
            </v-layout>
          </v-form>
        </template>
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
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { FarmProfile, FarmProfileUpdate } from '@/interfaces';
import { dispatchGetFarms, dispatchUpdateFarm } from '@/store/farm/actions';
import { readOneFarm } from '@/store/farm/getters';

@Component
export default class EditFarm extends Vue {
  public valid = false;
  public farm_name: string = '';
  public url: string = '';
  public username: string = '';
  public setPassword = false;
  public password1: string = '';
  public password2: string = '';

  public async mounted() {
    await dispatchGetFarms(this.$store);
    this.reset();
  }

  public reset() {
    this.setPassword = false;
    this.password1 = '';
    this.password2 = '';
    this.$validator.reset();
    if (this.farm) {
      this.farm_name = this.farm.farm_name;
      this.url = this.farm.url;
      this.username = this.farm.username;
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedFarm: FarmProfileUpdate = {};
      if (this.farm_name) {
        updatedFarm.farm_name = this.farm_name;
      }
      if (this.url) {
        updatedFarm.url = this.url;
      }
      if (this.username) {
        updatedFarm.username = this.username;
      }
      if (this.setPassword) {
        updatedFarm.password = this.password1;
      }
      await dispatchUpdateFarm(this.$store, { id: this.farm!.id, farm: updatedFarm });
      this.$router.push('/main/farm/farms');
    }
  }

  get farm() {
    return readOneFarm(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
