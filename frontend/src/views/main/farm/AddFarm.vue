<template xmlns="">
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Add a Farm</div>
      </v-card-title>

      <v-form v-model="valid" ref="form" lazy-validation>
        <v-card-text>
          <v-text-field label="Farm Name" v-model="farmName" required></v-text-field>
          <v-text-field label="URL" v-model="url" required></v-text-field>
          <v-text-field label="OAuth Scope" v-model="scope"></v-text-field>
          <v-text-field label="Notes (Optional)" v-model="notes"></v-text-field>
          <v-text-field label="Tags (Optional)" v-model="tags"></v-text-field>
          <div>
            <FarmTagsChips v-bind:tags="tags"/>
          </div>


          <div class="d-flex">
            <v-checkbox
                    v-model="active"
                    label="Active"
            ></v-checkbox>
          </div>
        </v-card-text>

        <FarmRequestRegistrationDialog
                ref="RequestRegistrationDialog"
        />

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="$refs.RequestRegistrationDialog.openDialog()">Request Registration</v-btn>
          <v-btn @click="cancel">Cancel</v-btn>
          <v-btn @click="reset">Reset</v-btn>
          <v-btn
                  color="primary"
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
import FarmRequestRegistrationDialog from '@/components/FarmRequestRegistrationDialog.vue';
import FarmTagsChips from '@/components/FarmTagsChips.vue';

@Component({
    components: {FarmRequestRegistrationDialog, FarmTagsChips},
})
export default class AddFarm extends Vue {
  public valid = false;
  public farmName: string = '';
  public url: string = '';
  public scope: string = '';
  public notes: string = '';
  public tags: string = '';
  public active: boolean = false;

  public async mounted() {
    await dispatchGetFarms(this.$store);
    this.reset();
  }

  public reset() {
    this.farmName = '';
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
        scope: this.scope,
        notes: this.notes,
        tags: this.tags,
        active: this.active,
      };
      await dispatchCreateFarm(this.$store, { data: updatedFarm }).then( (response) => {
        if (response) {
          this.$router.push('/main/farm/farms');
        }
      } );
    }
  }
}
</script>
