<script setup>
import { RouterLink, RouterView } from 'vue-router'
import UserBadge from "./components/UserBadge.vue";

</script>

<script >

import router from "./router";

export default {
  name: "App",
  data () {
    return {
      search: '',
    }
  },
  methods: {
    onMovieSearch() {
      router.push({name: 'movies-search', params: {search: this.search}})
      this.search = ''
    }
  }
}
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg bg-light text-font">
      <div class="container-fluid">
        <!-- Collapsible wrapper -->
        <div class="collapse navbar-collapse">
          <a href="/movies/" class="site-name" style="color: black; text-decoration: none; font-size: 28px"> Diploma IMDB </a>
        </div>
        <!-- Search form -->
        <div class="navbar-collapse d-flex align-items-center">
          <form class="input-group w-auto d-flex">
            <input
                class="form-control search-input"
                placeholder="Search"
                type="text"
                v-model="search"
            />

            <button
                class="btn btn-outline-secondary"
                type="submit"
                data-mdb-ripple-color="dark"
                @click="onMovieSearch"
            >
              Submit
            </button>
          </form>
          <div class="ms-auto">
            <UserBadge />
          </div>
        </div>

      </div>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
.text-font {
  font-family: Comic Sans MS, sans-serif;
}

/* Responsive styles */
@media screen and (max-width: 375px) {
  .search-input {
    min-width: 150px;
    max-width: 200px;
  }
}

@media screen and (max-width: 667px) {
  .site-name {
    display: block;
    font-size: 24px;
    margin-right: 10px;
  }

  .search-input {
    min-width: 200px;
    max-width: 250px;
  }
}

</style>
