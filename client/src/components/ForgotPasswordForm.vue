<script>
import { useQuasar } from 'quasar';
import { errorMessage } from '@/errors';

export default {
  name: 'ForgotPasswordForm',

  data() {
    return {
      user: {},
      formError: null,
      sending: false
    };
  },
  setup() {
    const $q = useQuasar();
    return { $q };
  },
  methods: {
    async onUserForgotPassword(e) {
      e.preventDefault();
      this.formError = null;
      this.sending = true;
      try {
        const response = await fetch('/api/v1/auth/password-reset/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.user.email })
        });
        if (response.status === 200) {
          this.positiveNotify((await response.json()).detail);
          this.user = {};
        } else {
          this.formError = await errorMessage(response);
          this.errorNotify();
        }
      } catch {
        this.formError = 'Network error';
        this.errorNotify();
      } finally {
        this.sending = false;
      }
    },
    positiveNotify(message) {
      this.$q.notify({
        message,
        color: 'positive',
        position: 'top',
        textColor: 'white',
        actions: [{ icon: 'close', color: 'white' }],
        timeout: 5000
      });
    },
    errorNotify() {
      this.$q.notify({
        message: this.formError,
        color: 'negative',
        position: 'top',
        textColor: 'white',
        actions: [{ icon: 'close', color: 'white' }],
        timeout: 2000
      });
    },
    goToLogin() {
      this.$router.push('/login/');
    },
    goToRegister() {
      this.$router.push('/register/');
    }
  }
};
</script>
<template>
  <div class="auth-form text-font">
    <div class="row justify-center items-center">
      <q-card class="q-pa-md q-ma-md" style="max-width: 400px; width: 100%">
        <q-card-section class="text-h5 text-center q-mb-md"> Forgot Password </q-card-section>
        <q-form @submit="onUserForgotPassword" class="q-gutter-md">
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
          <div class="text-center">
            <q-btn
              label="Send password reset"
              outline
              type="submit"
              :loading="sending"
              color="grey"
              class="form-button q-mb-md"
            ></q-btn>
          </div>
          <div class="row justify-between">
            <q-btn flat color="primary" no-caps label="Login" @click="goToLogin" />
            <q-btn flat color="primary" no-caps label="Register" @click="goToRegister" />
          </div>
        </q-form>
      </q-card>
    </div>
  </div>
</template>
