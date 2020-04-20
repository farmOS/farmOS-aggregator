<template>
  <v-container fluid>
    <v-card class="ma-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Farm</div>
      </v-card-title>

      <v-form v-model="valid" ref="form" lazy-validation>
        <v-card-text>
          <v-text-field label="Farm Name" v-model="farmName" required></v-text-field>
          <v-text-field label="URL" v-model="url" prefix="https://" required></v-text-field>
          <v-text-field label="OAuth Scope (readonly)" v-model="scope" readonly></v-text-field>
          <v-text-field label="Notes" v-model="notes" ></v-text-field>
          <v-text-field label="Tags" v-model="tags" ></v-text-field>
          <div>
            <FarmTagsChips v-bind:tags="tags"/>
          </div>
          <br>
          <FarmAuthorizationStatus v-bind:farm=farm></FarmAuthorizationStatus>

          <div class="d-flex">
            <v-checkbox
                    v-model="active"
                    label="Active"
            ></v-checkbox>
          </div>

          <v-expansion-panels
                  multiple
                  accordion
          >
            <v-expansion-panel
                    :disabled="!hasServerInfo"
            >
              <v-expansion-panel-header>
                farmOS Server Info
              </v-expansion-panel-header>

              <v-expansion-panel-content>
                <template v-if="hasServerInfo">
                  <v-text-field   label="Server Name" v-model="farm.info.name" readonly ></v-text-field>
                  <v-text-field   label="URL" v-model="farm.info.url" readonly ></v-text-field>
                  <v-text-field   label="API Version" v-model="farm.info.api_version" readonly ></v-text-field>
                  <v-text-field   v-if="hasAllServerInfo" label="System Of Measurement" v-model="farm.info.system_of_measurement" readonly ></v-text-field>
                  <v-text-field   v-if="hasAllServerInfo" label="Authorized User Email" v-model="farm.info.user.mail" readonly ></v-text-field>
                </template>
                <v-treeview
                        v-if="hasAllServerInfo"
                        dense
                        :items="this.resources"
                        :open-on-click="true"
                ></v-treeview>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel
                    :disabled = "!hasToken"
            >
              <v-expansion-panel-header>OAuth Token</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-text-field   label="Access Token" v-model="accessToken" readonly ></v-text-field>
                <v-text-field   label="Expires In" v-model="expiresIn" readonly ></v-text-field>
                <v-text-field   label="Expires At" v-model="expiresAt" readonly ></v-text-field>
                <v-text-field   label="Refresh Token" v-model="refreshToken" readonly ></v-text-field>

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
import { FarmProfileUpdate } from '@/interfaces';
import { dispatchGetFarms, dispatchUpdateFarm } from '@/store/farm/actions';
import { readOneFarm } from '@/store/farm/getters';
import Farm from '@/views/main/farm/Farm.vue';
import FarmAuthorizationStatus from '@/components/FarmAuthorizationStatus.vue';
import FarmTagsChips from '@/components/FarmTagsChips.vue';

@Component({
  components: {FarmTagsChips, FarmAuthorizationStatus, Farm},
})
export default class EditFarm extends Vue {
  public valid = false;
  public farmName: string = '';
  public url: string = '';
  public oldUrl: string = '';
  public scope: string = '';
  public notes: string = '';
  public tags: string = '';
  public active: boolean = false;

  public hasToken = false;
  public accessToken: string = '';
  public refreshToken: string = '';
  public expiresIn: string = '';
  public expiresAt: string = '';

  public hasServerInfo: boolean = false;
  public hasAllServerInfo: boolean = false;
  public resources: object[] = [];

  public async mounted() {
    await dispatchGetFarms(this.$store);
    this.reset();
  }

  public reset() {
    this.hasToken = false;
    this.$validator.reset();
    if (this.farm) {
      this.farmName = this.farm.farm_name;
      this.oldUrl = this.farm.url;
      this.url = this.farm.url;
      this.scope = this.farm.scope!;
      this.notes = this.farm.notes!;
      this.tags = this.farm.tags!;
      this.active = this.farm.active!;

      if (this.farm.token) {
        this.hasToken = true;
        this.accessToken = this.farm.token.access_token;
        this.refreshToken = this.farm.token.refresh_token;
        this.expiresIn = this.farm.token.expires_in;
        this.expiresAt = this.farm.token.expires_at;
      }
      if (this.farm.info) {
        this.hasServerInfo = true;
        /* tslint:disable:no-string-literal */
        if (this.farm.info['user'] !== null) {
          this.hasAllServerInfo = true;
          this.resources = this.buildResourcesTree(this.farm);
        }
      }
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedFarm: FarmProfileUpdate = {};
      if (this.farmName) {
        updatedFarm.farm_name = this.farmName;
      }
      // Only update the farm URL if it is different, avoid 409 error.
      if (this.url !== this.oldUrl) {
        updatedFarm.url = this.url;
      }
      if (this.notes) {
        updatedFarm.notes = this.notes;
      }
      if (this.tags) {
        updatedFarm.tags = this.tags;
      }

      updatedFarm.active = this.active;

      await dispatchUpdateFarm(this.$store, { id: this.farm!.id, farm: updatedFarm }).then( (result) => {
          if (result) {
              this.$router.push('/main/farm/farms');
          }
      });
    }
  }

  public buildResourcesTree(farm) {
    let i = 1;
    const output: object[] = [];
    if (farm.info) {
      for (const resource of Object.keys(farm.info.resources)) {
        const startID = i;
        i += 1;
        const child: object[] = [];
        for (const type of Object.keys(farm.info.resources[resource])) {
          child.push(
                  {id: i, name: type},
          );
          i += 1;
        }
        const res = {
          id: i,
          name: resource,
          children: child,
        };
        output.push(res);
        i += 1;
      }
    }

    return [ {id: 0, name: 'Resources', children: output}];
  }

  get farm() {
    return readOneFarm(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
