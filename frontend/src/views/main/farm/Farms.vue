<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Farms
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/farm/farms/add">Add a farm</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="farms" loading-text="Loading... Please wait">
      <template v-slot:item.is_authorized="{ item }">
        <FarmAuthorizationStatus v-bind:farm=item ></FarmAuthorizationStatus>
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
        <v-btn :to="{name: 'main-farm-farms-edit', params: {id: item.id}}">
          <v-icon>edit</v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { FarmProfile } from '@/interfaces';
import { readFarms } from '@/store/farm/getters';
import { dispatchGetFarms } from '@/store/farm/actions';
import FarmAuthorizationStatus from '@/components/FarmAuthorizationStatus.vue';

@Component({
    components: {FarmAuthorizationStatus},
})
export default class Farms extends Vue {
  public headers = [
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
      text: 'Last Accessed',
      sortable: true,
      value: 'last_accessed',
      align: 'left',
    },
    {
      text: 'Updated',
      sortable: true,
      value: 'time_updated',
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
  get farms() {
    return readFarms(this.$store);
  }

  public async mounted() {
    await dispatchGetFarms(this.$store);
  }
}
</script>
