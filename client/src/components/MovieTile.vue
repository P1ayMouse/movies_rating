<script setup>
import { QIcon } from 'quasar';
import PosterImage from './PosterImage.vue';
import { formatRating, yearOf } from '../format.js';

defineProps({
  movie: { type: Object, required: true }
});
</script>

<template>
  <router-link :to="{ name: 'movie', params: { id: movie.id } }" class="movie-tile">
    <div class="movie-tile-poster">
      <poster-image :src="movie.poster" icon-size="24px" />
    </div>
    <div class="movie-tile-info">
      <h3>{{ movie.name }}</h3>
      <p v-if="movie.year">{{ yearOf(movie.year) }}</p>
      <span v-if="formatRating(movie.average_rating)" class="movie-tile-rating">
        <q-icon class="popcorn-icon" size="18px" aria-hidden="true" />
        {{ formatRating(movie.average_rating) }}
        <span class="movie-tile-rating-scale">/ 10</span>
      </span>
      <span v-else class="movie-tile-unrated">Not yet rated</span>
    </div>
  </router-link>
</template>
