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
// import Pagination from './components/Pagination';
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
        baseUrl: "https://localhost:8080/search?",
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
      // const apiUrl = `${baseUrl}part=${part}&type=${type}&order=${order}&q=${q}&maxResults=${maxResults}&key=${key}`;
      const apiUrl = `${baseUrl}&q=${q}`;
      this.getData(apiUrl);
    },

    // prevPage() {
    //   const {
    //     baseUrl,
    //     part,
    //     type,
    //     order,
    //     maxResults,
    //     q,
    //     key,
    //     prevPageToken
    //   } = this.api;
    //   const apiUrl = `${baseUrl}part=${part}&type=${type}&order=${order}&q=${q}&maxResults=${maxResults}&key=${key}&pageToken=${prevPageToken}`;
    //   this.getData(apiUrl);
    // },

    // nextPage() {
    //   const {
    //     baseUrl,
    //     part,
    //     type,
    //     order,
    //     maxResults,
    //     q,
    //     key,
    //     nextPageToken
    //   } = this.api;
    //   const apiUrl = `${baseUrl}part=${part}&type=${type}&order=${order}&q=${q}&maxResults=${maxResults}&key=${key}&pageToken=${nextPageToken}`;
    //   this.getData(apiUrl);
    // },

    getData(apiUrl) {
      axios
        .get(apiUrl)
        .then(res => {
          if (this.data.status) {
            this.scholars = res.data.result;
          } else {
            // This is a little bit stupid ...
            setTimeout(function() {
              this.getData(apiUrl);
            }, 1000 * res.data.waiting);
          }
          // this.api.prevPageToken = res.data.prevPageToken;
          // this.api.nextPageToken = res.data.nextPageToken;
        })
        .catch(error => console.log(error));
    }
  }
};
</script>