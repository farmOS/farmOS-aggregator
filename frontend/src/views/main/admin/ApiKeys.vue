<template>
  <div>
    <v-data-table :headers="headers" :items="apiKeys" >
      <template v-slot:item.enabled="{ item } ">
        <v-simple-checkbox v-model="item.enabled" disabled/>
      </template>
      <template v-slot:item.all_farms="{ item } ">
        <v-simple-checkbox v-model="item.all_farms" disabled/>
      </template>
      <template v-slot:item.time_created="{ item }">
           <span v-if="item.time_created" >
                {{new Date(item.time_created).toLocaleString()}}
           </span>
      </template>
      <template v-slot:top>
        <v-toolbar flat color="white" light>
          <v-toolbar-title>Manage API Keys</v-toolbar-title>
          <v-divider
                  class="mx-4"
                  inset
                  vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">Edit API Key</span>
              </v-card-title>

              <v-card-text>
                <v-checkbox v-model="selectedApiKey.enabled" label="Enabled"></v-checkbox>
                <v-text-field v-model="selectedApiKey.name" label="Name"></v-text-field>
                <v-text-field v-model="selectedApiKey.notes" label="Notes"></v-text-field>
                <v-text-field v-model="new Date(selectedApiKey.time_created).toLocaleString()" label="Created" disabled></v-text-field>
                <v-text-field v-model="selectedApiKey.farm_id" label="Farm IDs" disabled></v-text-field>
                <v-text-field v-model="selectedApiKey.scopes" label="Scopes" disabled></v-text-field>
                <v-text-field v-model="selectedApiKey.key" label="Key" disabled></v-text-field>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="secondary" text @click="close">Cancel</v-btn>
                <v-btn color="primary" text @click="save">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.action="{ item }">
        <v-btn
                text
                icon
                @click="editApiKey(item)">
          <v-icon
                  class="mr-2"
          >
            edit
          </v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import { ApiKey } from '@/interfaces';
    import { readApiKeys} from '@/store/admin/getters';
    import { dispatchGetApiKeys } from '@/store/admin/actions';

    @Component
    export default class ApiKeys extends Vue {
        public dialog: boolean = false;
        public selectedApiKey = {} as ApiKey;

        public headers = [
            {
                text: 'Enabled',
                sortable: true,
                value: 'enabled',
                align: 'left',
            },
            {
                text: 'Key Name',
                sortable: true,
                value: 'name',
                align: 'left',
            },
            {
                text: 'Notes',
                sortable: true,
                value: 'notes',
                align: 'left',
            },
            {
                text: 'All Farms',
                sortable: true,
                value: 'all_farms',
                align: 'left',
            },
            {
                text: 'Farm IDs',
                sortable: true,
                value: 'farm_id',
                align: 'left',
            },
            {
                text: 'Scopes',
                sortable: true,
                value: 'scopes',
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

        public editApiKey(item) {
            this.selectedApiKey = Object.assign({}, item);
            this.dialog = true;
        }

        public save() {
            this.close();
        }

        public close() {
            this.dialog = false;
            this.selectedApiKey = Object.assign({}, {} as ApiKey);
        }

        get apiKeys() {
            return readApiKeys(this.$store);
        }

        public async mounted() {
            await dispatchGetApiKeys(this.$store);
        }
    }
</script>
