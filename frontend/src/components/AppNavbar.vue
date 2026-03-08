<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
    <span class="navbar-brand">
      HMS
    </span>

    <div class="collapse navbar-collapse show">
      <ul class="navbar-nav me-auto">

        <!-- ADMIN LINKS -->
        <li v-if="role === 'admin'" class="nav-item">
          <router-link class="nav-link" to="/admin">
            Dashboard
          </router-link>
        </li>

        <li v-if="role === 'admin'" class="nav-item">
          <router-link class="nav-link" to="/admin/doctors">
            Doctors
          </router-link>
        </li>

        <li v-if="role === 'admin'" class="nav-item">
          <router-link class="nav-link" to="/admin/departments">
            Departments
          </router-link>
        </li>

        <!-- DOCTOR LINKS -->
        <li v-if="role === 'doctor'" class="nav-item">
          <router-link class="nav-link" to="/doctor">
            Dashboard
          </router-link>
        </li>

        <li v-if="role === 'doctor'" class="nav-item">
          <router-link class="nav-link" to="/doctor/appointments">
            Appointments
          </router-link>
        </li>

        <!-- PATIENT LINKS -->
        <li v-if="role === 'patient'" class="nav-item">
          <router-link class="nav-link" to="/patient">
            Dashboard
          </router-link>
        </li>

        <li v-if="role === 'patient'" class="nav-item">
          <router-link class="nav-link" to="/patient/book">
            Book Appointment
          </router-link>
        </li>

        <li v-if="role === 'patient'" class="nav-item">
          <router-link class="nav-link" to="/patient/history">
            History
          </router-link>
        </li>

      </ul>

      <!-- LOGOUT -->
      <button
        class="btn btn-outline-light"
        @click="logout"
      >
        Logout
      </button>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    role() {
      return this.$store.state.auth.role
    }
  },
  methods: {
    async logout() {
      await this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    }
  }
}
</script>
