<template>
  <div id="app">
    <!-- Show navbar only if logged in -->
    <AppNavbar v-if="isAuthenticated" />
    <router-view />
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue'

export default {
  components: {
    AppNavbar
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token
    }
  }
}
</script>

<style>
body {
  margin: 0;
  background-color: #f8f9fa;
}
</style>
