<script>
import router from "../router"
import StarRating from 'vue-star-rating'

export default {
  name: 'MovieForm',
  data () {
    return {
      dataLoaded: false,
      formError: false,
      fullMovie: {},
      movie: {},
      persons: {},
      rating: {},
      isRatingCardOpen: false
    }
  },
  async mounted () {
    await this.fetchData();
  },
  watch: {
    '$route'() {
      this.fetchData();
    }
  },
  methods: {
    async fetchData() {
      this.dataLoaded = false
      const urlMovies = `/api/v1/movies/${this.$route.params.id}/`
      const urlPersonMovie = `/api/v1/movies/personmovies/?limit=100&search=${this.$route.params.id}`
      const urlRating = `/api/v1/movies/ratings/${this.$route.params.id}`

      Promise.all([
        fetch(urlMovies).then(response => response.json()),
        fetch(urlPersonMovie).then(response => response.json()),
        fetch(urlRating).then(response => response.json())
      ]).then(data => {
        const genres = data[0].genres.join(',');

        const urlTopThree = `/api/v1/movies/?limit=3&genre=${genres}&ordering=-rating__average_rating&ordering=id`;

        fetch(urlTopThree).then(response => response.json())
            .then(topThreeData => {
              this.movie = data[0];
              this.persons = data[1].results;
              this.rating = data[2];
              this.topThree = topThreeData.results;

              console.log(this.movie, this.persons, this.rating, this.topThree);

              document.title = `${this.movie.name} (${this.movie.imdb_id})`;

              this.dataLoaded = true;
            })
            .catch(error => {
              console.error(error);
            });
      }).catch(error => {
        console.error(error);
      });
    },
    onPersonPush(person) {
      router.push({name: 'person', params: {id: person.person_id.id}})
    },
    toggleRatingCard() {
      this.isRatingCardOpen = !this.isRatingCardOpen;
    },
    goToMovie(id) {
      router.push({ name: 'movie', params: { id }});
    },
    formatJob(job) {
      return job.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    },
    viewOnIMDb() {
      window.open(`https://www.imdb.com/title/${this.movie.imdb_id}`, '_blank');
    },
  },
  components: {
    StarRating
  }
};
</script>

<template>
  <div v-if="!dataLoaded">
    <div class="text-center m-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
  <div class="text-font m-4" v-if="dataLoaded">
    <div class="d-flex align-items">
      <div>
        <img :src="movie.poster ? movie.poster : '/src/components/icons/none_image.png'" class="card-img-top m-3" style="width:300px;">
        <div class="d-flex align-items-center justify-content-center">
          <star-rating :max-rating="10" :star-size="25" :show-rating="false" :rating="movie.average_rating" :increment="0.01" :read-only="true"/>
        </div>
        <p style="text-align: center; font-size: 14px;" class="mt-2" v-if="rating">based on {{ rating.num_votes }} rates</p>
        <div class="style-button mt-3">
          <button class="rating-card-button" @click="toggleRatingCard">Close/Open top 3 by genre</button>
        </div>
        <div class="style-button mt-3">
          <button @click="viewOnIMDb">View on IMDb</button>
        </div>
      </div>
      <div class="m-4">
        <h4>{{ movie.name }}</h4>
        <span v-if="movie.year" class="card-text" style="font-size: 12px;">{{ movie.year.substring(0, 4) }}</span>
        <span v-if="movie.year && movie.directors.length !== 0">, </span>
        <span v-for="(director, index) in movie.directors" style="font-size: 12px;" class="card-text">{{director}}{{index === movie.directors.length - 1 ? '' : ', '}}</span>
        <div class="mt-3">
          <span class="badge rounded-pill text-bg-secondary m-1" v-if="movie.genres" v-for="(genre, index) in movie.genres"> {{ genre }} </span>
        </div>
      </div>
    </div>
    <div style="width: 60%;">
      <table class="table table-striped" v-if="persons.length > 0">
        <thead>
        <tr>
          <th style="width: 1000px"> Name </th>
          <th style="width: 10px"> IMDB </th>
          <th style="width: 5px"> Age </th>
          <th style="width: 25%"> Job </th>
          <th style="width: 20%"> Roles </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(person, index) in persons" @click="onPersonPush(person)">
          <td style="width: 1000px">{{ person.person_id.name }}</td>
          <th style="width: 10px; font-weight: normal"> {{ person.person_id.imdb_id }} </th>
          <td style="width: 5px">{{ person.person_id.birth_year ? person.person_id.birth_year.slice(0, 4) : '' }}</td>
          <td style="width: 25%">{{ formatJob(person.category) }}</td>
          <td style="width: 20%"><span v-for="(character, index) in person.characters">{{ character }}<span v-if="index !== (person.characters.length - 1)">; </span></span></td>
        </tr>
        </tbody>
      </table>
    </div>
    <div class="rating-card" :style="{ right: isRatingCardOpen ? '0' : '-400px' }">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title" style="text-align: center">Top rated Like This</h5>
          <div class="card-group row row-cols-1 g-3">
            <div v-for="(movie, index) in topThree" @click="goToMovie(movie.id)" style="cursor: pointer;">
              <div class="card">
                <div class="card-body">
                  <img :src="movie.poster ? movie.poster : '/src/components/icons/none_image.png'" class="card-img-top d-block mx-auto mb-2" :alt="movie.name">
                  <div class="ms-2">
                    <p class="card-title mb-0" style="font-weight: bold; font-size: 14px;">{{ movie.name }}</p>
                    <div class="card-text mt-1" style="font-size: 10px">
                      <span v-if="movie.year" class="">{{ movie.year.substring(0, 4) }}</span>
                      <span v-if="movie.year && movie.directors.length !== 0">, </span>
                      <span v-for="(director, index) in movie.directors">{{director}}{{index === movie.directors.length - 1 ? '' : ', '}}</span>
                    </div>
                  </div>
                  <div>
                    <span class="badge rounded-pill text-bg-secondary mt-2 m-1" v-for="(genre, index) in movie.genres"> {{ genre }} </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.text-font {
  text-decoration: none;
  font-family: Comic Sans MS, sans-serif;
}
.rating-card {
  position: fixed;
  top: 53%;
  right: -400px; /* Початково ховаємо блок за межами екрану */
  transform: translateY(-50%);
  z-index: 999; /* Щоб блок був поверх інших елементів */
  transition: right 0.3s ease; /* Анімація відкриття/закриття блоку */
}

.rating-card .card {
  max-width: 280px; /* Задайте максимальну ширину карточки */
  border: none;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.rating-card .card-title {
  font-size: 16px; /* Зменште розмір шрифту заголовка */
  font-weight: bold;
  margin-bottom: 10px;
}

.rating-card .card-body {
  padding: 20px;
}

.card-img-top {
  border-radius: 10px !important;
}

@media screen and (max-height: 1350px), (max-width: 900px) {
  .rating-card, .rating-card-button {
    display: none;
  }
}

@media screen and (max-width: 576px) {
  .m-4 {
    margin: 0 auto;
    text-align: center;
  }
}

.rating-card .badge {
  background-color: #17a2b8;
  color: #fff;
  font-size: 10px; /* Зменште розмір шрифту для жанрів */
  padding: 5px 10px;
  margin-right: 5px;
  margin-bottom: 5px;
  border-radius: 20px;
}

.rating-card .card-img-top {
  width: 200px; /* Задайте бажаний розмір зображення */
}

.rating-card .card-text {
  font-size: 12px; /* Зменште розмір шрифту тексту */
}

.style-button {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
</style>