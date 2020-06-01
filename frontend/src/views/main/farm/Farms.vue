<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Farms
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
      <v-spacer></v-spacer>
        <div class="text-center">
          <v-btn
                  color="secondary"
                  class="ma-2"
                  @click="$refs.RequestRegistrationDialog.openDialog()"
          >
              Request Registration
          </v-btn>
          <FarmRequestRegistrationDialog
                  ref="RequestRegistrationDialog"
          />

          <v-btn
                  color="primary"
                  class="ma-2"
                  to="/main/farm/farms/add"
          >
            Add a farm
          </v-btn>
        </div>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="farms"
      :items-per-page="-1"
      :sort-by="'url'"
      :sort-desc="false"
      :search="search"
      :loading="loading"
      loading-text="Loading... Please wait"
    >
      <template v-slot:item.active="{ item } ">
        <v-simple-checkbox v-model="item.active" disabled/>
      </template>
      <template v-slot:item.is_authorized="{ item }">
        <FarmAuthorizationStatus v-bind:farm=item ></FarmAuthorizationStatus>
      </template>
      <template v-slot:item.tags="{ item }">
        <FarmTagsChips v-bind:tags="item.tags"/>
      </template>
      <template v-slot:item.last_accessed="{ item }">
           <span v-if="item.last_accessed" >
                {{new Date(item.last_accessed).toLocaleString()}}
           </span>
      </template>
      <template v-slot:item.time_updated="{ item }">
           <span v-if="item.time_updated" >
                {{new Date(item.time_updated).toLocaleString()}}
           </span>
      </template>
      <template v-slot:item.time_created="{ item }">
           <span v-if="item.time_created" >
                {{new Date(item.time_created).toLocaleString()}}
           </span>
      </template>
      <template v-slot:item.action="{ item }">
        <v-btn
          text
          icon
          :to="{name: 'main-farm-farms-edit', params: {id: item.id}}">
          <v-icon
            class="mr-2"
          >
            edit
          </v-icon>
        </v-btn>
        <v-btn
          text
          icon
          @click="loadFarmInfo(item.id)">
          <v-icon
            class="mr-2"
          >
            autorenew
          </v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readFarms } from '@/store/farm/getters';
import { dispatchGetFarms, dispatchGetFarmInfo, dispatchGetOneFarm } from '@/store/farm/actions';
import FarmAuthorizationStatus from '@/components/FarmAuthorizationStatus.vue';
import FarmRequestRegistrationDialog from '@/components/FarmRequestRegistrationDialog.vue';
import FarmTagsChips from '@/components/FarmTagsChips.vue';
import {FarmProfile} from '@/interfaces';

@Component({
    components: {FarmAuthorizationStatus, FarmRequestRegistrationDialog, FarmTagsChips},
})
export default class Farms extends Vue {
  public search = '';
  public headers = [
    {
        text: 'Active',
        sortable: true,
        value: 'active',
        align: 'left',
    },
    {
      text: 'Farm Name',
      sortable: true,
      value: 'farm_name',
      align: 'left',
    },
    {
      text: 'URL',
      sortable: true,
      value: 'url',
      align: 'left',
    },
    {
      text: 'Authorized',
      sortable: true,
      value: 'is_authorized',
      align: 'left',
    },
    {
        text: 'Tags',
        sortable: true,
        value: 'tags',
        align: 'left',
    },
    {
      text: 'API Version',
      sortable: true,
      value: 'info.api_version',
      align: 'left',
    },
    {
      text: 'Last Accessed',
      sortable: true,
      value: 'last_accessed',
      align: 'left',
    },
   {
      text: 'Created',
      sortable: true,
      value: 'time_created',
      align: 'left',
    },
    {
      text: 'Actions',
      sortable: false,
      value: 'action',
    },
  ];

  public loading: boolean = false;

  get farms() {
    return readFarms(this.$store);
  }

  public async mounted() {
    await dispatchGetFarms(this.$store);
  }

  public async loadFarmInfo(farmID) {
      this.loading = true;
      await dispatchGetFarmInfo(this.$store, {farmID}).then( (info) => {
            dispatchGetOneFarm(this.$store, {farmID}).then( (response) => {
                this.loading = false;
            });
          },

      );
  }
}
</script>
