<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Add a Farm</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Farm Name" v-model="farm_name" required></v-text-field>
            <v-text-field label="url" v-model="url" required></v-text-field>
            <v-text-field label="username" v-model="username" required></v-text-field>
            <v-text-field label="Notes (optional)" v-model="notes"></v-text-field>

            <v-layout align-center>
              <v-flex>
                <v-text-field type="password" ref="password" label="Set Password" data-vv-name="password" data-vv-delay="100" v-validate="{required: true}" v-model="password1" :error-messages="errors.first('password')">
                </v-text-field>
                <v-text-field type="password" label="Confirm Password" data-vv-name="password_confirmation" data-vv-delay="100" data-vv-as="password" v-validate="{required: true, confirmed: 'password'}" v-model="password2" :error-messages="errors.first('password_confirmation')">
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
        <v-btn @click="submit" :disabled="!valid">
              Save
            </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  FarmProfile,
  FarmProfileUpdate,
  FarmProfileCreate,
} from '@/interfaces';
import { dispatchGetFarms, dispatchCreateFarm } from '@/store/farm/actions';

@Component
export default class AddFarm extends Vue {
  public valid = false;
  public farm_name: string = '';
  public url: string = '';
  public username: string = '';
  public password1: string = '';
  public password2: string = '';
  public notes: string = '';

  public async mounted() {
    await dispatchGetFarms(this.$store);
    this.reset();
  }

  public reset() {
    this.password1 = '';
    this.password2 = '';
    this.farm_name = '';
    this.username = '';
    this.notes = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedFarm: FarmProfileCreate = {
        farm_name: this.farm_name,
        url: this.url,
        username: this.username,
        password: this.password1,
        notes: this.notes,
      };
      await dispatchCreateFarm(this.$store, updatedFarm);
      this.$router.push('/main/farm/farms');
    }
  }
}
</script>
