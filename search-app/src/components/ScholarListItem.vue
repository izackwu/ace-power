<template>
  <div>
    <div class="card-body">
      <h5 class="card-title">
        {{ scholar.author }}
        <!-- <a
          :href="'https://www.youtube.com/watch?v=' + scholar.id.scholarId"
          class="card-link"
          target="_blank"
        >{{ scholar.snippet.title }}</a>-->
      </h5>
      <h6 class="card-subtitle mb-2 text-muted">{{ scholar.affiliation }}</h6>
      <!-- <p class="card-text">{{ scholar.snippet.description }}</p> -->
    </div>
  </div>
</template>

<script>
export default {
  name: "ScholarListItem",
  props: ["scholar"]
};
</script>