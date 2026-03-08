<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="card shadow">
          <div class="card-header text-center">
            <h4>Hospital Management System</h4>
            <small class="text-muted">Login</small>
          </div>

          <div class="card-body">
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  v-model="email"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="password"
                  required
                />
              </div>

              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <button type="submit" class="btn btn-primary w-100">
                Login
              </button>
            </form>
          </div>

          <div class="card-footer text-center">
            <router-link to="/register">
              New patient? Register here
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',   // ✅ FIXED HERE
  data() {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async handleLogin() {
      try {
        this.error = null

        await this.$store.dispatch('auth/login', {
          email: this.email,
          password: this.password
        })

        const role = this.$store.state.auth.role

        if (role === 'admin') this.$router.push('/admin')
        else if (role === 'doctor') this.$router.push('/doctor')
        else if (role === 'patient') this.$router.push('/patient')
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          'Login failed. Try again.'
      }
    }
  }
}
</script>
