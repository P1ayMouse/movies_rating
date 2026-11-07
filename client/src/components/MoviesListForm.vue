<script>
import { QPagination, QSpinnerDots, QCard, QCardSection, QImg, QIcon, QChip } from 'quasar';

export default {
  name: 'MoviesListForm',
  components: {
    QPagination,
    QSpinnerDots,
    QCard,
    QCardSection,
    QImg,
    QIcon,
    QChip
  },
  data() {
    return {
      moviesLoaded: false,
      count: 0,
      page: 1,
      limit: 18,
      movies: [],
      search: '',
      directors: []
    };
  },
  async mounted() {
    await this.loadMovies();
    document.title = 'Diploma MDB';
  },
  watch: {
    page() {
      this.loadMovies();
    }
  },
  methods: {
    async loadMovies() {
      this.moviesLoaded = false;

      this.search = this.$route.params.search ? this.$route.params.search : '';

      const response_movies = await fetch(
        `/api/v1/movies/?limit=${this.limit}&offset=${(this.page - 1) * this.limit}&search=${this.search}&ordering=-rating__num_votes`,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      if (response_movies.status === 200) {
        const response_movies_Data = await response_movies.json();
        this.movies = response_movies_Data.results;
        this.count = response_movies_Data.count;
      }

      this.moviesLoaded = true;
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.count / this.limit);
    }
  }
};
</script>

<template>
  <div class="movies-list-page text-font">
    <div v-if="!moviesLoaded">
      <div class="spinner-container">
        <q-spinner-dots color="black" size="64px" />
      </div>
    </div>
    <div v-else class="movie-container">
      <div class="pagination-container" v-if="totalPages > 1">
        <q-pagination
          v-model="page"
          :max="totalPages"
          :max-pages="1"
          direction-links
          boundary-links
          :ellipses="false"
          :boundary-numbers="false"
          icon-first="skip_previous"
          icon-last="skip_next"
          icon-prev="fast_rewind"
          icon-next="fast_forward"
          class="pagination-mobile"
        />
      </div>
      <div class="movies-grid">
        <div v-for="movie in movies" :key="movie.id" class="movie-card-container">
          <q-card class="movie-card">
            <router-link :to="{ name: 'movie', params: { id: movie.id } }" class="movie-link">
              <q-img
                :src="
                  movie.poster && movie.poster !== 'None'
                    ? movie.poster
                    : '/src/components/icons/none_image.png'
                "
                class="movie-card-img"
              >
                <template v-slot:error>
                  <q-icon name="image_off" size="5em" />
                </template>
              </q-img>
              <q-card-section>
                <div class="movie-title">{{ movie.name }}</div>
                <div class="movie-details">
                  <span v-if="movie.year">{{ movie.year.substring(0, 4) }}</span>
                  <span v-if="movie.year && movie.directors.length !== 0">, </span>
                  <span v-for="(director, index) in movie.directors" :key="index"
                    >{{ director }}{{ index === movie.directors.length - 1 ? '' : ', ' }}</span
                  >
                </div>
                <div class="movie-genres">
                  <q-chip v-for="(genre, index) in movie.genres" :key="index" outline>{{
                    genre
                  }}</q-chip>
                </div>
              </q-card-section>
            </router-link>
          </q-card>
        </div>
      </div>

      <br /><br />

      <div class="pagination-container" v-if="totalPages > 1">
        <q-pagination
          v-model="page"
          :max="totalPages"
          :max-pages="6"
          direction-links
          boundary-links
          :ellipses="false"
          :boundary-numbers="false"
          icon-first="skip_previous"
          icon-last="skip_next"
          icon-prev="fast_rewind"
          icon-next="fast_forward"
          class="pagination-desktop"
        />
        <q-pagination
          v-model="page"
          :max="totalPages"
          :max-pages="1"
          direction-links
          boundary-links
          :ellipses="false"
          :boundary-numbers="false"
          icon-first="skip_previous"
          icon-last="skip_next"
          icon-prev="fast_rewind"
          icon-next="fast_forward"
          class="pagination-mobile"
        />
      </div>
      <div v-else-if="count === 0 && moviesLoaded" class="no-movies">
        <h2>Movies not found</h2>
      </div>
    </div>
  </div>
</template>
