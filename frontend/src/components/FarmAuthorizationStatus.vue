<template>
    <div>
        <v-btn
                v-if="farm.is_authorized"
                :to="{name: 'main-farm-farms-authorize', params: {id: farm.id}}"
                depressed
                small
                color="success"
        >
            Authorized
        </v-btn>
        <v-tooltip v-else bottom>
            <template v-slot:activator="{ on }">
                <v-btn
                        v-on="on"
                        :to="{name: 'main-farm-farms-authorize', params: {id: farm.id}}"
                        depressed
                        small
                        color="error"
                >
                    Re-Authorize
                    <v-icon right>error</v-icon>
                </v-btn>
            </template>
            <span>{{ farm.auth_error }}</span>
        </v-tooltip>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Emit } from 'vue-property-decorator';
import { FarmProfile } from '@/interfaces';

@Component
export default class FarmAuthorizationStatus extends Vue {
    @Prop({default: false}) public farm!: FarmProfile;

}
</script>

<style scoped>

</style>
