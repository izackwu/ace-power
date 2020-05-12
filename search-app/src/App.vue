<template>
  <div id="app">
    <Header />
    <SearchForm v-on:search="search" />
    <SearchResults
      v-if="scholars.length > 0"
      v-bind:scholars="scholars"
      v-bind:reformattedSearchString="reformattedSearchString"
    />
    <!-- <Pagination
      v-if="scholars.length > 0"
      v-bind:prevPageToken="api.prevPageToken"
      v-bind:nextPageToken="api.nextPageToken"
      v-on:prev-page="prevPage"
      v-on:next-page="nextPage"
    />-->
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */

import Header from "./components/layout/Header";
import SearchForm from "./components/SearchForm";
import SearchResults from "./components/SearchResults";
import axios from "axios";

export default {
  name: "app",
  components: {
    Header,
    SearchForm,
    SearchResults
    // Pagination
  },
  data() {
    return {
      scholars: [],
      reformattedSearchString: "",
      api: {
        baseUrl: "http://localhost:8000/search",
        part: "snippet",
        type: "video",
        order: "viewCount",
        maxResults: 12,
        q: "",
        key: "YOUR_API_KEY",
        prevPageToken: "",
        nextPageToken: ""
      }
    };
  },
  methods: {
    search(searchParams) {
      this.reformattedSearchString = searchParams.join(" ");
      this.api.q = searchParams.join("+");
      const { baseUrl, part, type, order, maxResults, q, key } = this.api;
      console.log(q);
      const apiUrl = `${baseUrl}/${q}`;
      this.getData(apiUrl);
    },

    getData(apiUrl) {
      axios
        .get(apiUrl)
        .then(res => {
          if (res.data.status) {
            this.scholars = res.data.result;
          } else {
            // This is a little bit stupid ...
            setTimeout(() => {
              this.getData(apiUrl);
            }, 1000 * res.data.waiting);
          }
        })
        .catch(error => console.log(error));
    }
  }
};
</script>
