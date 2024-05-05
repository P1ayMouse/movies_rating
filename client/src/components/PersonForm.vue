<script>
export default {
  name: 'PersonForm',
  data () {
    return {
      personLoaded: false,
      person: {}
    }
  },
  async mounted () {
    this.personLoaded = false
    const urlPersonMovie = `/api/v1/movies/persons/?search=${this.$route.params.id}`;

    try {
      const response = await fetch(urlPersonMovie);
      const data = await response.json();

      this.person = data.results[0];

      // Отримання даних про known_for_titles
      await Promise.all(this.person.known_for_titles.map(async (imdb_id) => {
        const movieUrl = `/api/v1/movies/?search=${imdb_id}`;
        const movieResponse = await fetch(movieUrl);
        const movieData = await movieResponse.json();
        if (movieData.results.length > 0) {
          // Якщо фільм знайдено, додайте його до об'єкту person
          if (!this.person.knownForMovies) {
            this.person.knownForMovies = [];
          }
          this.person.knownForMovies.push(movieData.results[0]);
        }
      }));

      console.log(this.person);
      this.personLoaded = true;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    goToMoviePage(movieId) {
      this.$router.push(`/movies/movie/${movieId}`);
    }
  }

};
</script>


<template>
  <div v-if="!personLoaded">
    <div class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>

  <div class="text-font m-4" v-if="personLoaded">
    <div class="d-flex align-items">
      <img src="./icons/none_image.png" class="card-img-top m-3 " style="width:300px;">
      <div class="m-4">
        <h4> {{ person.name }} </h4>
        <span style="font-size: 12px;" v-if="person.birth_year"> {{ person.birth_year ? person.birth_year.slice(0, 4) : '' }}  </span>
        <span style="font-size: 12px;" v-if="person.death_year && person.birth_year"> - {{ person.death_year.slice(0, 4) }} </span>

      </div>
    </div>
    <div style="width: 70%;">
      <table class="table table-striped" v-if="person.knownForMovies && person.knownForMovies.length > 0">
        <thead>
        <tr>
          <th> Name </th>
          <th> IMDB </th>
          <th> Average rating </th>
          <th> Genres </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(movie, index) in person.knownForMovies" @click="goToMoviePage(movie.id)">
          <td style="width: 30%">{{ movie.name }}</td>
          <td style="width: 10%">{{ movie.imdb_id }}</td>
          <td style="width: 15%"> {{ movie.average_rating }} </td>
          <td><span v-for="(genre, index) in movie.genres">{{ genre }}<span v-if="index !== (movie.genres.length - 1)">; </span></span></td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.text-font {
  text-decoration: none;
  font-family: Comic Sans MS, sans-serif;
}
table {
  width: 70%;
}
</style>
