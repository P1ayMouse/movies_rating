<script>
import { QBtn, QIcon, QInput } from 'quasar';
import PasswordInput from './PasswordInput.vue';
import { APP_NAME } from '../brand.js';
import { logIn, nextPath } from '@/auth';

export default {
  name: 'LoginForm',
  components: { PasswordInput, QBtn, QIcon, QInput },
  data() {
    return {
      appName: APP_NAME,
      email: '',
      password: '',
      loading: false,
      formError: ''
    };
  },
  methods: {
    async onLogin() {
      this.formError = '';
      if (!this.email.trim() || !this.password) {
        this.formError = 'Enter your email and password.';
        return;
      }

      this.loading = true;
      try {
        this.formError = await logIn(this.email.trim(), this.password);
        if (!this.formError) this.$router.push(nextPath(this.$route));
      } catch {
        this.formError = 'Network error. Please try again.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div class="auth-page">
    <div v-reveal class="auth-card">
      <h1 class="auth-title">Welcome back</h1>
      <p class="auth-subtitle">Log in to {{ appName }} to rate movies and manage your account.</p>

      <form class="auth-fields" novalidate @submit.prevent="onLogin">
        <q-input
          v-model="email"
          outlined
          type="email"
          label="Email"
          autocomplete="email"
          autofocus
        />

        <div>
          <password-input v-model="password" />
          <router-link :to="{ name: 'password-forgot' }" class="auth-forgot">
            Forgot password?
          </router-link>
        </div>

        <p v-if="formError" class="auth-error" role="alert">
          <q-icon name="error_outline" size="18px" aria-hidden="true" />
          {{ formError }}
        </p>

        <q-btn
          type="submit"
          unelevated
          no-caps
          label="Log in"
          class="auth-submit"
          :loading="loading"
        />
      </form>

      <p class="auth-footer">
        New to {{ appName }}?
        <router-link :to="{ name: 'register', query: $route.query }">Create an account</router-link>
      </p>
    </div>
  </div>
</template>
