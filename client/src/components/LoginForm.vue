<script>
import { useQuasar } from 'quasar';

export default {
  name: 'LoginForm',
  data() {
    return {
      user: {},
      formError: null,
    };
  },
  setup() {
    const $q = useQuasar();
    return { $q };
  },
  methods: {
    async onUserLogin(e) {
      e.preventDefault();
      this.formError = null;
      const response = await fetch('/api/v1/auth/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.user),
      });
      console.log(response);

      if (response.status !== 200) {
        try {
          this.formError = (await response.json()).detail;
        } catch {
          this.formError = 'Unknown error';
        }
        this.errorNotify();
      } else {
        const response_data = await response.json();
        localStorage.setItem('movies_rating-access', response_data.access);
        localStorage.setItem('movies_rating-refresh', response_data.refresh);
        this.$router.push('/profile');

      }
    },
    errorNotify() {
      this.$q.notify({
        message: this.formError,
        color: 'negative',
        position: 'top',
        textColor: 'white',
        actions: [{ icon: 'close', color: 'white'}],
        html: true,
        timeout: 2000,
      });
    },
    goToRegister() {
      this.$router.push('/register/')
    },
    goToPasswordForgot() {
      this.$router.push('/password-forgot/')
    }
  },
};
</script>

<template>
  <div class="text-font">
    <div class="d-flex justify-content-center align-items-center">
      <q-card class="q-pa-md q-ma-md" style="max-width: 400px; width: 100%;">
        <q-card-section class="text-h5 text-center q-mb-md">
          Login
        </q-card-section>
        <q-form @submit="onUserLogin" class="q-gutter-md">
          <q-input
              outlined
              v-model="user.email"
              placeholder="Input your email"
              type="email"
              label="e-mail"
              required
              color="grey"
              class="q-mb-md"
          />
          <q-input
              outlined
              v-model="user.password"
              placeholder="Input your password"
              type="password"
              label="password"
              required
              color="grey"
              class="q-mb-md"
          />
          <div class="text-center">
            <q-btn label="Log In" outline type="submit" color="grey" class="form-button q-mb-md"></q-btn>
          </div>
          <div class="d-flex justify-content-between">
            <q-btn
                flat
                color="primary"
                no-caps
                label="Forgot password"
                class="float-start"
                @click="goToPasswordForgot"
            />
            <q-btn
                flat
                color="primary"
                no-caps
                label="Register"
                class="float-end"
                @click="goToRegister"
            />
          </div>
        </q-form>
      </q-card>
    </div>
  </div>
</template>

<style scoped>
.text-font {
  text-decoration: none;
  font-family: 'Comic Sans MS', sans-serif;
  color: black;
}
.form-button {
  border-radius: 5px;
}
</style>
