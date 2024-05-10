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
        <!-- Site name -->
        <a href="/movies/" class="site-name"> Diploma IMDB </a>

        <!-- Search form -->
        <div class="d-flex justify-content-center flex-grow-1">
          <form class="input-group" style="max-width: 400px;">
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
        </div>

        <!-- User badge -->
        <div class=" d-flex justify-content-center user-badge">
          <UserBadge />
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

.site-name {
  margin-bottom: 10px;
  margin-right: 30px;
  color: black;
  text-decoration: none;
  font-size: 28px
}
.search-input {
  min-width: 200px;
  max-width: 250px;
}

/* Responsive styles */
@media screen and (max-width: 667px) {
  .site-name {
    margin-bottom: 20px;
  }

  .container-fluid {
    display: flex;
    flex-direction: column;
  }
  .user-badge{
  margin-top: 10px;

  }
}
</style>
