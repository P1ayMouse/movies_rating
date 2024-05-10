<script >

export default {
  name: "MoviesListForm",
  data () {
    return {
      moviesLoaded: false,
      personsLoaded: false,
      count: 0,
      page: 1,
      limit: 18,
      movies: [],
      search: '',
      directors: []
    }
  },
  async mounted() {
    await this.loadMovies();
    document.title = 'Diploma IMDB';
  },

  methods: {
    async changePage(newPage) {
      if (newPage >= 1 && newPage <= this.totalPages && newPage !== this.page) {
        this.page = newPage;
        await this.loadMovies();
      }
    },
    async loadMovies() {
      this.moviesLoaded = false

      this.search = this.$route.params.search ? this.$route.params.search : ''

      const response_movies = await fetch(`/api/v1/movies/?limit=${this.limit}&offset=${(this.page-1) * this.limit}&search=${this.search}`, {
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
    },
  },
  computed: {
    totalPages() {
      return Math.ceil(this.count / this.limit);
    },
    visiblePages() {
      const visiblePageCount = 5; // Кількість видимих сторінок
      let startPage = Math.max(1, this.page - Math.floor(visiblePageCount / 2));
      let endPage = Math.min(this.totalPages, startPage + visiblePageCount - 1);

      // Переконайтеся, що ми відображаємо правильну кількість сторінок, навіть якщо `totalPages` менше `visiblePageCount`
      if (endPage - startPage + 1 < visiblePageCount) {
        startPage = Math.max(1, endPage - visiblePageCount + 1);
      }

      return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
    }
  },


}
</script>

<template>
  <div class="text-font">
    <div v-if="!moviesLoaded">
      <div class="text-center m-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
    <div v-else class="m-4">
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 row-cols-xxl-6 g-4">
        <div v-for="(movie, index) in movies" :key="movie.id" class="col">
          <div class="card h-100">
            <router-link :to="{name: 'movie', params: {id: movie.id}}" style="text-decoration: none; color: black">
              <div class="card-body">
                <img src="./icons/none_image.png" class="card-img-top mb-2">
                <div class="ms-2">
                  <p class="card-title mb-0" style="font-weight: bold; font-size: 18px;">{{ movie.name }}</p>
                  <div class="card-text mt-1" style="font-size: 12px">
                    <span v-if="movie.year">{{ movie.year.substring(0, 4) }}</span>
                    <span v-if="movie.year && movie.directors.length !== 0">, </span>
                    <span v-for="(director, index) in movie.directors">{{ director }}{{ index === movie.directors.length - 1 ? '' : ', ' }}</span>
                  </div>
                </div>
                <div>
                  <span class="badge rounded-pill text-bg-secondary mt-2 m-1" v-for="(genre, index) in movie.genres" :key="index"> {{ genre }} </span>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>

      <br><br>
      <nav aria-label="Page navigation" v-if="totalPages > 1">
        <div class="d-flex justify-content-center">
          <ul class="pagination">
            <li class="page-item" :class="{disabled: page === 1}">
              <a class="page-link" href="#" aria-label="Previous" @click="changePage(page - 1)">
                <span aria-hidden="true"> &laquo; </span>
              </a>
            </li>
            <template v-if="totalPages >= 10">
              <!-- Показуємо сторінки від 1 до 5 -->
              <template v-if="page <= 4 || totalPages <= 5">
                <template v-for="pageNum in [1, 2, 3, 4, 5, 6, '...', totalPages]" :key="pageNum">
                  <li class="page-item" :class="{active: page === pageNum}">
                    <a class="page-link" href="#" @click="changePage(pageNum)">{{ pageNum }}</a>
                  </li>
                </template>
              </template>

              <!-- Показуємо поточну сторінку та останні чотири сторінки -->
              <template v-else-if="page > totalPages - 4">
                <template v-for="pageNum in [1, '...', totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages]" :key="pageNum">
                  <li class="page-item" :class="{active: page === pageNum}">
                    <a class="page-link" href="#" @click="changePage(pageNum)" v-if="pageNum !== '...'">{{ pageNum }}</a>
                    <span class="page-link" v-else>{{ pageNum }}</span>
                  </li>
                </template>
              </template>

              <!-- Показуємо середину списку сторінок -->
              <template v-else>
                <template v-for="pageNum in [1, '...', page - 1, page, page + 1, '...', totalPages]" :key="pageNum">
                  <li class="page-item" :class="{active: page === pageNum}">
                    <a class="page-link" href="#" @click="changePage(pageNum)" v-if="pageNum !== '...'">{{ pageNum }}</a>
                    <span class="page-link" v-else>{{ pageNum }}</span>
                  </li>
                </template>
              </template>
            </template>
            <template v-else>
        <template v-for="pageNum in totalPages" :key="pageNum">
          <li class="page-item" :class="{active: page === pageNum}">
            <a class="page-link" href="#" @click="changePage(pageNum)">{{ pageNum }}</a>
          </li>
        </template>
            </template>
            <li class="page-item" :class="{disabled: page === totalPages}">
              <a class="page-link" href="#" aria-label="Next" @click="changePage(page + 1)">
                <span aria-hidden="true"> &raquo; </span>
              </a>
            </li>
          </ul>
        </div>
      </nav>

      <div v-else-if="count === 0 && moviesLoaded" style="text-align: center">
        <h1>Movies no found</h1>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-font {
  text-decoration: none;
  font-family: Comic Sans MS, sans-serif;
}
</style>

