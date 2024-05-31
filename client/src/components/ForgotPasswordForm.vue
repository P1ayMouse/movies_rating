<script>
import {useQuasar} from "quasar";

export default {
  name: "ForgotPasswordForm",

  data() {
    return {
      user: {},
      formError: null
    }
  },
  setup() {
    const $q = useQuasar();
    return { $q };
  },
  methods: {
    async onUserForgotPassword(e) {
      e.preventDefault();
      this.formError = null;
    },
    positiveNotify() {
      this.$q.notify({
        message: 'Password reset link sent!',
        color: 'positive',
        position: 'top',
        textColor: 'white',
        actions: [{ icon: 'close', color: 'white' }],
        html: true,
        timeout: 2000,
      });
    },
    errorNotify() {
      this.$q.notify({
        message: this.formError,
        color: 'negative',
        position: 'top',
        textColor: 'white',
        actions: [{ icon: 'close', color: 'white' }],
        html: true,
        timeout: 2000,
      });
    },
    goToLogin() {
      this.$router.push('/login/');
    },
    goToRegister() {
      this.$router.push('/register/');
    },
  }
}

</script>
<template>
  <div class="text-font">
    <div class="d-flex justify-content-center align-items-center">
      <q-card class="q-pa-md q-ma-md" style="max-width: 400px; width: 100%;">
        <q-card-section class="text-h5 text-center q-mb-md">
          Forgot Password
        </q-card-section>
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
            <q-btn label="Send password reset" outline type="submit" color="grey" class="form-button q-mb-md"></q-btn>
          </div>
          <div class="d-flex justify-content-between">
            <q-btn
                flat
                color="primary"
                no-caps
                label="Login"
                class="float-start"
                @click="goToLogin"
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