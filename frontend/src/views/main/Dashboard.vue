<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Dashboard</div>
      </v-card-title>
      <v-card-text>
        <div class="headline ma-3">Welcome {{greetedUser}}</div>
        <div class="body2 font-weight ">
          <p>
            This is the dashboard page of farmOS-aggregator. Use the menu on the left
            or some of the options below to view and manage farmOS profiles.
          </p>
        </div>
      </v-card-text>
      <v-card-text>
      <ul>
        <li>
          <a href="https://farmos.org/">farmOS.org</a>
        </li>
        <li>
          <a href="https://github.com/farmOS/farmOS-aggregator/blob/master/docs/using-farmos-aggregator.md">farmOS-aggregator documentation</a>
        </li>
        <li>
          <a href="https://github.com/farmOS/farmOS-aggregator">farmOS-aggregator Code Repository</a>
        </li>
      </ul>


      </v-card-text>
    </v-card>

    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Farm Profiles</div>
      </v-card-title>

      <v-card-text>
        <div class="subheading">Manage farmOS profiles</div>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" to="/main/farm/farms/">
          Manage Farms
          <v-icon right dark>list</v-icon>
        </v-btn>
        <v-btn
          color="secondary"
          class="ma-2"
          @click="$refs.RequestRegistrationDialog.openDialog()"
        >
          Request Registration
          <v-icon right dark>send</v-icon>
        </v-btn>
        <FarmRequestRegistrationDialog
          ref="RequestRegistrationDialog"
        />
        <v-btn color="accent" to="/main/farm/farms/add">
          Add Farm
          <v-icon right dark>add</v-icon>
        </v-btn>
      </v-card-actions>

    </v-card>

    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">User Profiles</div>
      </v-card-title>

      <v-card-text>
        <div class="subheading">Manage user profiles</div>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/main/profile/view">
          View Profile
          <v-icon right dark>info</v-icon>
        </v-btn>
        <v-btn to="/main/profile/edit">
          Edit Profile
          <v-icon right dark>edit</v-icon>
        </v-btn>
        <v-btn to="/main/profile/password">
          Change Password
          <v-icon right dark>edit</v-icon>
        </v-btn>
      </v-card-actions>

    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readUserProfile } from '@/store/main/getters';
import FarmRequestRegistrationDialog from '@/components/FarmRequestRegistrationDialog.vue';
import FarmAuthorizationStatus from '@/components/FarmAuthorizationStatus.vue';

@Component({
    components: {FarmRequestRegistrationDialog},
})
export default class Dashboard extends Vue {
  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile && userProfile.full_name) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
  }
}
</script>
