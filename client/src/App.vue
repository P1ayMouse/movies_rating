<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import UserBadge from './components/UserBadge.vue';

const search = ref('');
const router = useRouter();

const onMovieSearch = () => {
  if (search.value.trim()) {
    router.push({ name: 'movies-search', params: { search: search.value.trim() } });
    search.value = '';
  }
};
</script>

<template>
  <header>
    <nav class="site-header text-font">
      <div class="site-header-inner row justify-between items-center">
        <!-- Site name -->
        <a href="/movies/" class="site-name"> Diploma MDB </a>

        <!-- Centered search form -->
        <div class="search-area row justify-center">
          <form class="row no-wrap items-center form-container">
            <input
              v-model="search"
              type="text"
              placeholder="Search"
              class="search-input"
              @keyup.enter="onMovieSearch"
            />
            <button type="submit" class="search-button" @click="onMovieSearch">
              <q-icon name="search" />
            </button>
          </form>
        </div>

        <!-- User badge -->
        <div class="user-badge">
          <UserBadge />
        </div>
      </div>
    </nav>
  </header>

  <RouterView class="text-font" />
</template>
