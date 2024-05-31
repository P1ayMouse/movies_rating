<script>
import {
  QPagination, QSpinnerDots, QCard, QCardSection, QImg, QIcon, QChip,
  QToolbar, QToolbarTitle, QInput, QBtn, QSpace, QPage, QPageContainer, QLayout
} from 'quasar'

export default {
  name: 'MoviesListForm',
  components: {
    QPagination, QSpinnerDots, QCard, QCardSection, QImg, QIcon, QChip,
    QToolbar, QToolbarTitle, QInput, QBtn, QSpace, QPage, QPageContainer, QLayout
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
    }
  },
  async mounted() {
    await this.loadMovies()
    document.title = 'Diploma MDB'
  },
  watch: {
    page() {
      this.loadMovies()
    }
  },
  methods: {
    async loadMovies() {
      this.moviesLoaded = false

      this.search = this.$route.params.search ? this.$route.params.search : ''

      const response_movies = await fetch(`/api/v1/movies/?limit=${this.limit}&offset=${(this.page - 1) * this.limit}&search=${this.search}&ordering=-rating__num_votes`, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response_movies.status === 200) {
        const response_movies_Data = await response_movies.json()
        this.movies = response_movies_Data.results
        this.count = response_movies_Data.count
      }

      this.moviesLoaded = true
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.count / this.limit)
    }
  }
}
</script>

<template>
  <div class="text-font">
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
        <div v-for="(movie, index) in movies" :key="movie.id" class="movie-card-container">
          <q-card class="movie-card">
            <router-link :to="{ name: 'movie', params: { id: movie.id } }" class="movie-link">
              <q-img :src="(movie.poster && movie.poster !== 'None') ? movie.poster : '/src/components/icons/none_image.png'" class="card-img-top">
                <template v-slot:error>
                  <q-icon name="image_off" size="5em" />
                </template>
              </q-img>
              <q-card-section>
                <div class="movie-title">{{ movie.name }}</div>
                <div class="movie-details">
                  <span v-if="movie.year">{{ movie.year.substring(0, 4) }}</span>
                  <span v-if="movie.year && movie.directors.length !== 0">, </span>
                  <span v-for="(director, index) in movie.directors" :key="index">{{ director }}{{ index === movie.directors.length - 1 ? '' : ', ' }}</span>
                </div>
                <div class="movie-genres">
                  <q-chip v-for="(genre, index) in movie.genres" :key="index" outline>{{ genre }}</q-chip>
                </div>
              </q-card-section>
            </router-link>
          </q-card>
        </div>
      </div>

      <br><br>

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

<style scoped>
.text-font {
  text-decoration: none;
  font-family: Comic Sans MS, sans-serif;
}

.spinner-container {
  text-align: center;
  margin: 50px 0;
}

.movie-container {
  padding: 20px;
}

.movies-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.movie-card-container {
  flex: 1 1 calc(20% - 20px);
  max-width: 300px;
  display: flex;
  justify-content: center;
}

.movie-card {
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  border-radius: 10px;
  overflow: hidden;
}

.movie-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.movie-link {
  text-decoration: none;
  color: inherit;
}

.card-img-top {
  height: 400px;
  object-fit: cover;
  border-bottom: 1px solid #eee;
}

.movie-title {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 5px;
}

.movie-details {
  font-size: 0.9em;
  color: #555;
}

.movie-genres {
  margin-top: 10px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination-desktop {
  display: none;
}

.pagination-mobile {
  display: block;
  margin-right: 25%;
  margin-bottom: 20px;
}

.no-movies {
  text-align: center;
  margin: 20px 0;
}

@media (min-width: 577px) {
  .pagination-desktop {
    display: block;
  }

  .pagination-mobile {
    display: none;
  }
}

@media (max-width: 1200px) {
  .movie-card-container {
    flex: 1 1 calc(25% - 20px);
  }
}

@media (max-width: 992px) {
  .movie-card-container {
    flex: 1 1 calc(33.33% - 20px);
  }
}

@media (max-width: 768px) {
  .movie-card-container {
    flex: 1 1 calc(50% - 20px);
  }
}

@media (max-width: 576px) {
  .movie-card-container {
    flex: 1 1 calc(100% - 20px);
  }
}
</style>
