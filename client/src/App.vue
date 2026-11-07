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

<style>
body {
  color: #212529;
  background-color: #fff;
}
</style>

<style scoped>
.site-header {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  background-color: #f8f9fa;
}

.site-header-inner {
  width: 100%;
  padding: 0 0.75rem;
}

.search-area {
  flex-grow: 1;
}

.text-font {
  font-family:
    Comic Sans MS,
    sans-serif;
}

.search-input {
  border: 1px solid #ccc;
  border-radius: 10px 0 0 10px;
  padding: 5px 10px;
  width: 100%;
  box-sizing: border-box;
}

.search-input:focus {
  border-color: #999;
  outline: none;
}

.search-button {
  border: 1px solid #ccc;
  border-left: none;
  border-radius: 0 10px 10px 0;
  padding: 5px 10px;
  background-color: white;
  cursor: pointer;
}

.form-container {
  width: 100%;
  max-width: 300px;
  display: flex;
}

.site-name {
  color: black;
  text-decoration: none;
  font-size: 28px;
  white-space: nowrap;
}

.user-badge {
  margin-left: 20px;
}

@media screen and (max-width: 767px) {
  .site-name {
    margin-bottom: 10px;
    margin-top: 10px;
  }

  .site-header-inner {
    flex-direction: column;
  }

  .form-container {
    width: 100%;
  }

  .user-badge {
    margin-bottom: 10px;
    margin-top: 10px;
  }
}
</style>
