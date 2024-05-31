<script>
import { useQuasar } from 'quasar';
import axios from "axios";

export default {
  name: 'RegisterForm',
  data() {
    return {
      user: {
        email: '',
        password: '',
        password2: '',
        username: ''
      },
      formError: null,
    };
  },
  setup() {
    const $q = useQuasar();
    return { $q };
  },
  methods: {
    async onUserRegister(e) {
      e.preventDefault();
      this.formError = null;

      await axios.get("/sanctum/csrf-cookie");

      const response = await fetch("/api/v1/auth/user-registration/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.user),
      });
      console.log(response);

      const responseData = await response.json();

      if (response.status === 201) {
        this.positiveNotify()
        this.$router.push("/login");
      } else {
        switch (response.status) {
          case 400:
            if (responseData.detail !== undefined) {
              this.formError = responseData.detail;
            } else if (responseData.email !== undefined) {
              this.formError = responseData.email[0];
            } else if (responseData.username !== undefined) {
              this.formError = responseData.username[0];
            } else {
              this.formError = "Unknown error";
            }
            break;
          default:
            this.formError = "Unknown error";
            break;
        }
        this.errorNotify();
      }
    },
    positiveNotify() {
      this.$q.notify({
        message: 'Register is successful!',
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
  },
};
</script>

<template>
  <div class="text-font">
    <div class="d-flex justify-content-center align-items-center">
      <q-card class="q-pa-md q-ma-md" style="max-width: 400px; width: 100%;">
        <q-card-section class="text-h5 text-center q-mb-md">
          Register
        </q-card-section>
        <q-form @submit="onUserRegister" class="q-gutter-md">
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
          <q-input
              outlined
              v-model="user.password2"
              placeholder="Repeat password"
              type="password"
              label="repeat password"
              required
              color="grey"
              class="q-mb-md"
          />
          <q-input
              outlined
              v-model="user.username"
              placeholder="Input your username"
              label="username"
              required
              color="grey"
              class="q-mb-md"
          />
          <div class="text-center">
            <q-btn label="Register" outline type="submit" color="grey" class="form-button q-mb-md"></q-btn>
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
.notification {
  word-wrap: break-word;
  white-space: pre-wrap;
}
</style>
