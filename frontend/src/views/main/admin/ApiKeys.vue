<template>
  <div>
    <v-data-table :headers="headers" :items="apiKeys" >
      <template v-slot:item.enabled="{ item } ">
        <v-simple-checkbox v-model="item.enabled" disabled/>
      </template>
      <template v-slot:item.all_farms="{ item } ">
        <v-simple-checkbox v-model="item.all_farms" disabled/>
      </template>
      <template v-slot:item.farm_id="{ item }">
        <v-chip-group
          column
        >
          <v-chip v-for="farm in item.farm_id" :key="farm" x-small>
            {{ farm }}
          </v-chip>
        </v-chip-group>
      </template>
      <template v-slot:item.scopes="{ item }">
        <v-chip-group
          column
        >
          <v-chip v-for="scope in item.scopes" :key="scope" x-small pill>
            {{ scope }}
          </v-chip>
        </v-chip-group>
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
          <v-dialog v-model="dialog" persistent max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on">New API Key</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">Edit API Key</span>
              </v-card-title>

              <v-card-text v-if="'id' in selectedApiKey">
                <v-checkbox v-model="selectedApiKey.enabled" label="Enabled"></v-checkbox>
                <v-text-field v-model="selectedApiKey.name" label="Name"></v-text-field>
                <v-text-field v-model="selectedApiKey.notes" label="Notes"></v-text-field>
                <v-text-field v-model="new Date(selectedApiKey.time_created).toLocaleString()" label="Created" disabled></v-text-field>
                <v-textarea v-model="selectedApiKey.key" label="Key" auto-grow readonly></v-textarea>
                <v-checkbox v-model="selectedApiKey.all_farms" label="All Farms" disabled></v-checkbox>
                <v-select
                  v-model="selectedApiKey.farm_id"
                  :items="farms"
                  item-text="farm_name"
                  item-value="id"
                  :menu-props="{ maxHeight: '400' }"
                  label="Farms"
                  multiple
                  hint="farmOS Server this API key will have access to."
                  persistent-hint
                  small-chips
                  readonly
                  outlined
                ></v-select>
                <v-select
                  v-model="selectedApiKey.scopes"
                  :items="aggregatorScopes"
                  item-text="label"
                  item-value="id"
                  :menu-props="{ maxHeight: '400' }"
                  label="Scopes"
                  multiple
                  hint="Scoped access for this API Key."
                  persistent-hint
                  small-chips
                  readonly
                  outlined
                ></v-select>
              </v-card-text>
              <v-card-text v-else>
                <v-checkbox v-model="newApiKey.enabled" label="Enabled"></v-checkbox>
                <v-text-field v-model="newApiKey.name" label="Name"></v-text-field>
                <v-text-field v-model="newApiKey.notes" label="Notes"></v-text-field>
                <v-checkbox v-model="newApiKey.all_farms" label="All Farms"></v-checkbox>
                <v-select
                  v-model="newApiKey.farm_id"
                  :items="farms"
                  item-text="farm_name"
                  item-value="id"
                  :menu-props="{ maxHeight: '400' }"
                  label="Farms"
                  multiple
                  hint="farmOS Server this API key will have access to."
                  persistent-hint
                  small-chips
                  outlined
                ></v-select>
                <v-select
                  v-model="newApiKey.scopes"
                  :items="aggregatorScopes"
                  item-text="label"
                  item-value="id"
                  :menu-props="{ maxHeight: '400' }"
                  label="Scopes"
                  multiple
                  hint="Scoped access for this API Key."
                  persistent-hint
                  small-chips
                  outlined
                ></v-select>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="secondary" text @click="close">Cancel</v-btn>
                <v-btn color="primary" text @click="save">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="confirmDeleteDialog" persistent max-width="450">
            <v-card>
              <v-card-title class="headline">Delete API Key '{{ selectedApiKey.name }}' ?</v-card-title>
              <v-card-text>Any service using this key to access the Aggregator will be blocked. Make sure services have a new API key in place.</v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="secondary" text @click="close">Cancel</v-btn>
                <v-btn color="primary" text @click="deleteApiKey">Delete</v-btn>
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
        <v-btn
                text
                icon
                @click="promptDeleteApiKey(item)">
          <v-icon
                  class="mr-2"
          >
            delete
          </v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import { ApiKey, ApiKeyCreate, ApiKeyUpdate } from '@/interfaces';
    import { readApiKeys} from '@/store/admin/getters';
    import { dispatchGetApiKeys, dispatchCreateApiKey, dispatchUpdateApiKey, dispatchDeleteApiKey } from '@/store/admin/actions';
    import { readFarms } from '@/store/farm/getters';
    import { dispatchGetFarms } from '@/store/farm/actions';


    @Component
    export default class ApiKeys extends Vue {
        public dialog: boolean = false;
        public confirmDeleteDialog: boolean = false;
        public selectedApiKey = {} as ApiKey;
        public newApiKeyDefault = {
          enabled: true,
          name: '',
          notes: '',
          all_farms: false,
          farm_id: [],
          scopes: [],
        } as ApiKeyCreate;
        public newApiKey = Object.assign({}, this.newApiKeyDefault);

        public aggregatorScopes = [
          {
            id: 'farm:read',
            label: 'Read farm profiles',
          },
          {
            id: 'farm:create',
            label: 'Create farm profiles',
          },
          {
            id: 'farm:update',
            label: 'Update farm profiles',
          },
          {
            id: 'farm:delete',
            label: 'Delete farm profiles',
          },
          {
            id: 'farm:authorize',
            label: 'Authorize farm profiles',
          },
          {
            id: 'farm.info',
            label: 'Read farmOS server info',
          },
        ];

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

        public promptDeleteApiKey(item) {
          this.selectedApiKey = Object.assign({}, item);
          this.confirmDeleteDialog = true;
        }

        public deleteApiKey() {
          if ('id' in this.selectedApiKey) {
            dispatchDeleteApiKey(this.$store, { id: this.selectedApiKey.id }).then(() => {
              this.close();
            });
          }
        }

        public save() {
          if ('id' in this.selectedApiKey) {
            const updateValues: ApiKeyUpdate = {
              enabled: this.selectedApiKey.enabled,
              name: this.selectedApiKey.name,
              notes: this.selectedApiKey.notes,
            };
            dispatchUpdateApiKey(this.$store, { id: this.selectedApiKey.id, apiKey: updateValues }).then(() => {
              this.close();
            });
          } else {
            const newValues: ApiKeyCreate = {
              enabled: this.newApiKey.enabled,
              name: this.newApiKey.name,
              notes: this.newApiKey.notes,
              all_farms: this.newApiKey.all_farms,
              farm_id: this.newApiKey.farm_id,
              scopes: this.newApiKey.scopes,
            };
            dispatchCreateApiKey(this.$store, newValues).then(() => {
              this.close();
            });
          }
        }

        public close() {
            this.dialog = false;
            this.confirmDeleteDialog = false;
            this.selectedApiKey = Object.assign({}, {} as ApiKey);
            this.newApiKey = Object.assign({}, this.newApiKeyDefault);
        }

        get apiKeys() {
            return readApiKeys(this.$store);
        }

        get farms() {
            return readFarms(this.$store);
        }

        public async mounted() {
            await dispatchGetApiKeys(this.$store);
            await dispatchGetFarms(this.$store);
        }
    }
</script>
