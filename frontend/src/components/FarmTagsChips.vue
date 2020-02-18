<template>
 <span>
    <v-chip
      v-if="tagList[0] != ''"
      v-for="tag in tagList"
      :key="tag"
      class="ma-2"
      color="secondary"
      small
    >
      {{ tag }}
    </v-chip>
 </span>
</template>

<script lang="ts">
import {Component, Vue, Prop, Emit, Watch} from 'vue-property-decorator';

@Component
export default class FarmTagsChips extends Vue {
    @Prop({default: ''}) public tags!: string;

    get tagList() {
        return this.tags.split(' ');
    }
}
</script>

<style scoped>

</style>
