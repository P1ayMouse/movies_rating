<script setup>
import { pageTitle } from '../brand.js';
import LoginForm from '../components/LoginForm.vue';
document.title = pageTitle('Login');
</script>

<template>
  <main>
    <LoginForm />
  </main>
</template>
