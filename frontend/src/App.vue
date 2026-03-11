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

  /* Global background image */
  background: url("@/assets/new.png") no-repeat center center fixed;

  /* make image cover full screen */
  background-size: cover;

  /* fallback color if image not loaded */
  background-color: #f8f9fa;
}

/* make cards readable on top of background */
.card {
  background: rgba(255,255,255,0.95);
}
</style>