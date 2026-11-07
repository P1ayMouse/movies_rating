<script>
import { useQuasar } from 'quasar';
import { loadCurrentUser, saveTokens } from '@/auth';

export default {
  name: 'LoginForm',
  data() {
    return {
      user: {},
      formError: null
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
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.user)
      });

      if (response.status !== 200) {
        try {
          this.formError = (await response.json()).detail;
        } catch {
          this.formError = 'Unknown error';
        }
        this.errorNotify();
      } else {
        saveTokens(await response.json());
        await loadCurrentUser();
        this.$router.push('/profile');
      }
    },
    errorNotify() {
      this.$q.notify({
        message: this.formError,
        color: 'negative',
        position: 'top',
        textColor: 'white',
        actions: [{ icon: 'close', color: 'white' }],
        html: true,
        timeout: 2000
      });
    },
    goToRegister() {
      this.$router.push('/register/');
    },
    goToPasswordForgot() {
      this.$router.push('/password-forgot/');
    }
  }
};
</script>

<template>
  <div class="auth-form text-font">
    <div class="row justify-center items-center">
      <q-card class="q-pa-md q-ma-md" style="max-width: 400px; width: 100%">
        <q-card-section class="text-h5 text-center q-mb-md"> Login </q-card-section>
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
            <q-btn
              label="Log In"
              outline
              type="submit"
              color="grey"
              class="form-button q-mb-md"
            ></q-btn>
          </div>
          <div class="row justify-between">
            <q-btn
              flat
              color="primary"
              no-caps
              label="Forgot password"
              @click="goToPasswordForgot"
            />
            <q-btn flat color="primary" no-caps label="Register" @click="goToRegister" />
          </div>
        </q-form>
      </q-card>
    </div>
  </div>
</template>
