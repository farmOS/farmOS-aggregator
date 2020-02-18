<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Dashboard</div>
      </v-card-title>
      <v-card-text>
        <div class="headline ma-3">Welcome {{greetedUser}}</div>
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

        <div class="d-flex flex-row justify-center text-center">
          <div class="pa-5">
            <p class="display-2 font-weight-bold pt-4">
              {{ totalFarms }}
            </p>
            <p class="headline font-weight-bold">
              Total Farms
            </p>
          </div>
          <div class="pa-5">
            <v-progress-circular
              :rotate="-90"
              :size="100"
              :width="15"
              :value="(activeFarms/totalFarms)*100"
              color="primary"
            >
              {{ activeFarms }} / {{ totalFarms}}
            </v-progress-circular>
            <p class="headline font-weight-bold">
              Active Farms
            </p>
          </div>
          <div class="pa-5">
            <v-progress-circular
              :rotate="-90"
              :size="100"
              :width="15"
              :value="(authorizedFarms/activeFarms)*100"
              color="secondary"
            >
              {{ authorizedFarms }} / {{ activeFarms}}
            </v-progress-circular>
            <p class="headline font-weight-bold">
              Authorized Farms
            </p>
          </div>
          <div class="pa-5" v-if="unauthorizedFarms > 0">
            <v-progress-circular
              :rotate="-90"
              :size="100"
              :width="15"
              :value="(unauthorizedFarms/activeFarms)*100"
              color="red"
            >
              {{ unauthorizedFarms }} / {{ activeFarms}}
            </v-progress-circular>
            <p class="headline font-weight-bold">
              Unauthorized Farms!
            </p>
          </div>
        </div>

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
import {readFarms} from '@/store/farm/getters';

@Component({
    components: {FarmRequestRegistrationDialog},
})
export default class Dashboard extends Vue {
  public totalFarms: number = 0;
  public activeFarms: number = 0;
  public inactiveFarms: number = 0;
  public authorizedFarms: number = 0;
  public unauthorizedFarms: number = 0;

  public async mounted() {
      this.totalFarms = this.farms.length;
      this.activeFarms = this.farms.filter((farm) => farm.active).length;
      this.inactiveFarms = this.farms.filter((farm) => !farm.active).length;
      this.authorizedFarms = this.farms.filter((farm) => farm.active && farm.is_authorized).length;
      this.unauthorizedFarms = this.farms.filter((farm) => farm.active && !farm.is_authorized).length;
  }

  get farms() {
      return readFarms(this.$store);
  }

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
