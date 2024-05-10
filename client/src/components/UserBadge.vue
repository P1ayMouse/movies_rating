<template>
  <div v-if="!userLoaded" class="text-font">
    Loading...
  </div>
  <div v-else-if="user !== null" class="dropdown text-font" style="text-decoration: none; color: black;">
    <button class="btn dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
      <img src="./icons/account-circle-512.webp" height="30" class="m-2">
      {{ user.username }}
    </button>
    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
      <li><a class="dropdown-item" style="margin-bottom: 0.5rem;" @click="doEditAccount()">Edit Account</a></li>
      <li><a class="dropdown-item" @click="doMoviesList()">Movies List</a></li>
      <hr style="margin-top: 0.5rem; margin-bottom: 0.5rem;">
      <li><a class="dropdown-item" @click="doLogOut()">Log Out</a></li>
    </ul>
  </div>
  <div v-else class="text-font">
    <RouterLink to="/login/"> Log In </RouterLink>
  </div>
</template>

<script>
export default {
  name: "UserBadge",
  data() {
    return {
      user: null,
      userLoaded: false
    }
  },
  async mounted() {
    const token = localStorage.getItem('movies_rating-access')
    let user = null

    const response = await fetch('/api/v1/auth/user-info/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.status === 200) {
      user = await response.json()
    }
    else if (response.status === 403) {
      // try to renew token
      const newTokenResponse = await fetch('/api/v1/auth/refresh/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({'refresh': localStorage.getItem('movies_rating-refresh')})
          }
      )
      if (newTokenResponse.status === 200 ) {
        localStorage.setItem('movies_rating-access', (await newTokenResponse.json()).access)
        // retry last api call
      }
      else {
        localStorage.removeItem('movies_rating-access')
        localStorage.removeItem('movies_rating-refresh')
      }
    }
    else {
      user = {email: 'Error'}
    }

    this.user = user
    this.userLoaded = true
  },
  methods: {
    doLogOut() {
      localStorage.removeItem('movies_rating-access')
      localStorage.removeItem('movies_rating-refresh')
      this.user = null
      this.$router.push('/login')
    },
    doEditAccount() {
      this.$router.push('/profile')
    },
    doMoviesList() {
      this.$router.push('/movies')
    }
  }
}

</script>

<style scoped>

</style>