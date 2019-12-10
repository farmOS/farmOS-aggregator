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
        <v-btn
                v-else
                :to="{name: 'main-farm-farms-authorize', params: {id: farm.id}}"
                depressed
                small
                color="error"
        >
            Re-Authorize
            <v-icon right>error</v-icon>
        </v-btn>
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
