<script>
import { QBtn, QIcon, QInput } from 'quasar';
import PasswordInput from './PasswordInput.vue';
import { APP_NAME } from '../brand.js';
import { logIn, nextPath } from '@/auth';
import { errorMessage } from '@/errors';

const MIN_LENGTH = 6;

export default {
  name: 'RegisterForm',
  components: { PasswordInput, QBtn, QIcon, QInput },
  data() {
    return {
      appName: APP_NAME,
      username: '',
      email: '',
      password: '',
      password2: '',
      loading: false,
      formError: ''
    };
  },
  methods: {
    // Same rules as the server, checked first so people don't wait for a request
    validate() {
      if (!this.username.trim() || !this.email.trim() || !this.password || !this.password2) {
        return 'Fill in all fields.';
      }
      if (this.username.trim().length < MIN_LENGTH) {
        return `Username must be at least ${MIN_LENGTH} characters.`;
      }
      if (!this.email.includes('@')) return 'Enter a valid email.';
      if (this.password.length < MIN_LENGTH) {
        return `Password must be at least ${MIN_LENGTH} characters.`;
      }
      if (this.password !== this.password2) return 'Passwords do not match.';
      return '';
    },
    async onRegister() {
      this.formError = this.validate();
      if (this.formError) return;

      this.loading = true;
      try {
        const email = this.email.trim();
        const response = await fetch('/api/v1/auth/user-registration/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username.trim(),
            email,
            password: this.password,
            password2: this.password2
          })
        });
        if (!response.ok) {
          this.formError = await errorMessage(response);
          return;
        }

        // Log straight in, so people don't have to type the password again
        const loginError = await logIn(email, this.password);
        if (loginError) {
          this.$router.push({ name: 'login', query: this.$route.query });
          return;
        }
        this.$q.notify({
          message: `Welcome to ${this.appName}!`,
          color: 'positive',
          position: 'top',
          timeout: 2000
        });
        this.$router.push(nextPath(this.$route));
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
      <h1 class="auth-title">Create an account</h1>
      <p class="auth-subtitle">Join {{ appName }} in a minute.</p>

      <form class="auth-fields" novalidate @submit.prevent="onRegister">
        <q-input
          v-model="username"
          outlined
          label="Username"
          autocomplete="nickname"
          maxlength="150"
          autofocus
        />
        <q-input v-model="email" outlined type="email" label="Email" autocomplete="email" />
        <password-input v-model="password" autocomplete="new-password" />
        <password-input v-model="password2" label="Repeat password" autocomplete="new-password" />

        <p v-if="formError" class="auth-error" role="alert">
          <q-icon name="error_outline" size="18px" aria-hidden="true" />
          {{ formError }}
        </p>

        <q-btn
          type="submit"
          unelevated
          no-caps
          label="Create account"
          class="auth-submit"
          :loading="loading"
        />
      </form>

      <p class="auth-footer">
        Already have an account?
        <router-link :to="{ name: 'login', query: $route.query }">Log in</router-link>
      </p>
    </div>
  </div>
</template>
