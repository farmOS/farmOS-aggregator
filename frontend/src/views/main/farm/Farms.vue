<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Farms
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/farm/farms/add">Add a farm</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="farms">
      <template slot="items" slot-scope="props">
       <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-farm-farms-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
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

@Component
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
      text: 'Username',
      sortable: true,
      value: 'username',
      align: 'left',
    },
    {
      text: 'Notes',
      sortable: true,
      value: 'notes',
      align: 'left',
    },
    {
      text: 'Time Updated',
      sortable: true,
      value: 'time_updated',
      align: 'left',
    },
    {
      text: 'Time Created',
      sortable: true,
      value: 'time_created',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
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
