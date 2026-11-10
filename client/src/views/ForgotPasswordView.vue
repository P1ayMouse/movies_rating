<script setup>
import { pageTitle } from '../brand.js';
import ForgotPasswordForm from '../components/ForgotPasswordForm.vue';
document.title = pageTitle('Forgot password');
</script>

<template>
  <main>
    <ForgotPasswordForm />
  </main>
</template>
