<script>
export default {
  name: "ProfileForm",

  data() {
    return {
      user: {
      },
      userLoaded: false,
      formError: null,
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
      document.title = 'Profile of ' + user.username;
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
    }
    else {
      user = {email: 'Error'}
    }

    this.user = user
    this.userLoaded = true
  },
  methods: {
    async onUserEditProfile(e) {
      e.preventDefault();
      this.formError = null;
    },
  }
}
</script>

<template>
  <div>
    <div v-if="formError" class="alert alert-danger" role="alert">
      {{ formError }}
    </div>
    <div class="d-flex justify-content-center m-5">
      <form @submit.prevent="onUserEditProfile" class="col-12 col-md-6">
        <br>
        <div class="mb-4">
          <label class="form-label">E-mail:</label>
          <input type="email" name="email" class="form-control" v-model="user.email" readonly placeholder="Input your email">
        </div>
        <div class="mb-4">
          <label class="form-label">Username:</label>
          <input name="username" class="form-control" v-model="user.username" placeholder="Input your username">
        </div>
        <div class="mb-4">
          <label class="form-label">Password:</label>
          <input type="password" name="password" class="form-control" v-model="user.password" placeholder="Input your password">
        </div>
        <div class="mb-4">
          <label class="form-label">Repeat password:</label>
          <input type="password" name="password2" class="form-control" v-model="user.password2" placeholder="Repeat your password">
        </div>
        <div class="d-flex justify-content-center">
          <input type="submit" class="btn btn-outline-secondary m-4" value="Update">
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
  .col-12.col-md-6 {
    width: 400px;
  }
</style>
