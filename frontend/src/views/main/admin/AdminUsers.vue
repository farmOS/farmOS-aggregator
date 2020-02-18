<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Users
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/users/create">Create User</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="users">
      <template v-slot:item.is_active="{ item } ">
         <v-simple-checkbox v-model="item.is_active" disabled/>
      </template>
      <template v-slot:item.is_superuser="{ item } ">
        <v-simple-checkbox v-model="item.is_superuser" disabled/>
      </template>
      <template v-slot:item.action="{ item }">
        <v-btn
          text
          icon
          :to="{name: 'main-admin-users-edit', params: {id: item.id}}"
        >
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
import { Store } from 'vuex';
import { IUserProfile } from '@/interfaces';
import { readAdminUsers } from '@/store/admin/getters';
import { dispatchGetUsers } from '@/store/admin/actions';

@Component
export default class AdminUsers extends Vue {
  public headers = [
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left',
    },
    {
      text: 'Full Name',
      sortable: true,
      value: 'full_name',
      align: 'left',
    },
    {
      text: 'Is Active',
      sortable: true,
      value: 'is_active',
      align: 'left',
    },
    {
      text: 'Is Superuser',
      sortable: true,
      value: 'is_superuser',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'action',
    },
  ];
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }
}
</script>
