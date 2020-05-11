<template>
  <div class="container mb-3">
    <div class="d-flex mb-3">
      <div class="mr-auto">
        <h3>Search Results for "{{ reformattedSearchString }}"</h3>
      </div>
      <!-- <div class="btn-group ml-auto" role="group">
        <button
          @click="changeDisplayMode('grid')"
          type="button"
          class="btn btn-outline-secondary"
          v-bind:class="{ active: displayMode === 'grid' }"
        >
          <i class="fas fa-th"></i>
        </button>
        <button
          @click="changeDisplayMode('list')"
          type="button"
          class="btn btn-outline-secondary"
          v-bind:class="{ active: displayMode === 'list' }"
        >
          <i class="fas fa-list"></i>
        </button>
      </div>-->
    </div>

    <div class="card-columns" v-if="displayMode === 'grid'">
      <div class="card" v-bind:key="scholar.author" v-for="scholar in scholars">
        <ScholarGridItem v-bind:scholar="scholar" />
      </div>
    </div>
    <div v-else>
      <div class="card mb-2" v-bind:key="scholar.author" v-for="scholar in scholars">
        <ScholarListItem v-bind:scholar="scholar" />
      </div>
    </div>
  </div>
</template>

<script>
import ScholarListItem from "./ScholarListItem";
// import ScholarGridItem from './ScholarGridItem';

export default {
  name: "SearchResults",
  components: {
    ScholarListItem
    // ScholarGridItem
  },
  data() {
    return {
      title: "Search Results",
      displayMode: "list"
    };
  },
  //   methods: {
  //     changeDisplayMode(displayMode) {
  //       this.displayMode = displayMode;
  //     }
  //   },
  props: ["scholars", "reformattedSearchString"]
};
</script>

<style scoped>
button:focus {
  box-shadow: none !important;
}
</style>