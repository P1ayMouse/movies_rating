<script>
import { pageTitle } from '../brand.js';
import { QBtn, QIcon, QSpinnerDots } from 'quasar';
import MoviePagination from './MoviePagination.vue';
import PosterImage from './PosterImage.vue';
import { formatRating, voteLabel, yearOf } from '../format.js';

const numberFormat = new Intl.NumberFormat('en-US');

export default {
  name: 'MoviesList',
  components: { MoviePagination, PosterImage, QBtn, QIcon, QSpinnerDots },
  data() {
    return {
      loading: true,
      errorMessage: '',
      count: 0,
      page: 1,
      limit: 18,
      movies: [],
      requestId: 0
    };
  },
  computed: {
    search() {
      return (this.$route.params.search || '').trim();
    },
    totalPages() {
      return Math.ceil(this.count / this.limit);
    },
    pageTitle() {
      return this.search ? `Results for “${this.search}”` : 'Popular movies';
    },
    countLabel() {
      const total = `${numberFormat.format(this.count)} ${this.count === 1 ? 'movie' : 'movies'}`;
      return this.search ? `${total} found` : `${total}, most voted first`;
    }
  },
  watch: {
    page() {
      this.loadMovies();
      window.scrollTo({ top: 0 });
    },
    // The same component is reused when a new search is made from the header
    search() {
      if (this.page === 1) this.loadMovies();
      else this.page = 1;
    }
  },
  mounted() {
    this.loadMovies();
  },
  beforeUnmount() {
    this.requestId += 1;
  },
  methods: {
    async loadMovies() {
      const requestId = ++this.requestId;
      this.loading = true;
      this.errorMessage = '';
      document.title = pageTitle(this.search);

      const params = new URLSearchParams({
        limit: this.limit,
        offset: (this.page - 1) * this.limit,
        search: this.search,
        ordering: '-rating__num_votes'
      });

      try {
        const response = await fetch(`/api/v1/movies/?${params}`);
        if (!response.ok) throw new Error('Movies request failed');
        const data = await response.json();
        if (requestId !== this.requestId) return;
        this.movies = data.results;
        this.count = data.count;
      } catch {
        if (requestId !== this.requestId) return;
        this.errorMessage = 'We could not load movies. Please try again.';
      } finally {
        if (requestId === this.requestId) this.loading = false;
      }
    },
    movieMeta(movie) {
      const year = yearOf(movie.year);
      const genres = (movie.genres || []).slice(0, 2).join(', ');
      return [year, genres].filter(Boolean).join(' · ');
    },
    formatRating,
    voteLabel
  }
};
</script>

<template>
  <div class="movies-list-page">
    <header class="movies-list-header">
      <div>
        <h1>{{ pageTitle }}</h1>
        <p v-if="count && !errorMessage" class="movies-list-count">{{ countLabel }}</p>
      </div>
      <router-link v-if="search" :to="{ name: 'movies' }" class="movies-list-clear">
        <q-icon name="close" size="18px" aria-hidden="true" />
        Clear search
      </router-link>
    </header>

    <div v-if="loading && !movies.length" class="movies-list-status" role="status">
      <q-spinner-dots color="grey-8" size="40px" aria-hidden="true" />
      <p>Loading movies…</p>
    </div>

    <div v-else-if="errorMessage" class="movies-list-status" role="alert">
      <h2>Unable to load movies</h2>
      <p>{{ errorMessage }}</p>
      <q-btn outline no-caps label="Try again" @click="loadMovies" />
    </div>

    <div v-else-if="!loading && count === 0" class="movies-list-status">
      <q-icon name="search_off" size="40px" aria-hidden="true" />
      <h2>No movies found</h2>
      <p v-if="search">Nothing matches “{{ search }}”. Check the spelling or try another title.</p>
      <router-link v-if="search" :to="{ name: 'movies' }" class="movies-list-browse">
        Browse all movies
      </router-link>
    </div>

    <template v-else>
      <div v-if="totalPages > 1" class="pagination-container pagination-container--top">
        <movie-pagination v-model="page" :total-pages="totalPages" />
      </div>

      <ul class="movies-grid" :class="{ 'is-loading': loading }" :aria-busy="loading">
        <li v-for="(movie, index) in movies" :key="movie.id" v-reveal="index">
          <router-link :to="{ name: 'movie', params: { id: movie.id } }" class="movie-card">
            <div class="movie-card-poster">
              <poster-image :src="movie.poster" icon-size="32px" label="No poster" />

              <span
                v-if="formatRating(movie.average_rating)"
                class="movie-card-rating"
                :aria-label="`Rating ${formatRating(movie.average_rating)} out of 10`"
              >
                <q-icon class="popcorn-icon" size="16px" aria-hidden="true" />
                {{ formatRating(movie.average_rating) }}
              </span>

              <!-- Short details that slide up over the poster on hover -->
              <div class="movie-card-details" aria-hidden="true">
                <p class="movie-card-details-rating">
                  <template v-if="formatRating(movie.average_rating)">
                    <q-icon class="popcorn-icon" size="20px" />
                    {{ formatRating(movie.average_rating) }}
                    <span>/ 10</span>
                  </template>
                  <template v-else>Not yet rated</template>
                </p>
                <p v-if="Number(movie.num_votes) > 0" class="movie-card-details-votes">
                  {{ voteLabel(movie.num_votes) }}
                </p>
                <p v-if="movie.directors?.length" class="movie-card-details-directors">
                  Directed by {{ movie.directors.join(', ') }}
                </p>
                <ul v-if="movie.genres?.length" class="movie-card-details-genres">
                  <li v-for="genre in movie.genres" :key="genre">{{ genre }}</li>
                </ul>
              </div>
            </div>

            <h2 class="movie-card-title">{{ movie.name }}</h2>
            <p v-if="movieMeta(movie)" class="movie-card-meta">{{ movieMeta(movie) }}</p>
          </router-link>
        </li>
      </ul>

      <div v-if="totalPages > 1" class="pagination-container">
        <movie-pagination v-model="page" :total-pages="totalPages" />
      </div>
    </template>
  </div>
</template>
