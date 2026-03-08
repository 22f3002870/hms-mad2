<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="card shadow">
          <div class="card-header text-center">
            <h4>Patient Registration</h4>
          </div>

          <div class="card-body">
            <form @submit.prevent="registerPatient">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="form.name"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  v-model="form.email"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="form.password"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Age</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="form.age"
                />
              </div>

              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <div v-if="success" class="alert alert-success">
                Registration successful! You can login now.
              </div>

              <button type="submit" class="btn btn-success w-100">
                Register
              </button>
            </form>
          </div>

          <div class="card-footer text-center">
            <router-link to="/login">
              Already have an account? Login
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api/axios'

export default {
  name: 'RegisterView',
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        age: ''
      },
      error: null,
      success: false
    }
  },
  methods: {
    async registerPatient() {
      try {
        this.error = null
        this.success = false

        await api.post('/patient/register', this.form)

        this.success = true
        this.form = {
          name: '',
          email: '',
          password: '',
          age: ''
        }
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          'Registration failed'
      }
    }
  }
}
</script>
