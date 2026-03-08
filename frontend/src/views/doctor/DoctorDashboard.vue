<template>
  <div class="container mt-4">
    <h2 class="mb-4">Doctor Dashboard</h2>

    <div class="row">
      <div class="col-md-4">
        <div class="card bg-primary text-white mb-3">
          <div class="card-body text-center">
            <h5>Total Appointments</h5>
            <h2>{{ stats.total_appointments }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card bg-success text-white mb-3">
          <div class="card-body text-center">
            <h5>Completed</h5>
            <h2>{{ stats.completed }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card bg-warning text-dark mb-3">
          <div class="card-body text-center">
            <h5>Pending</h5>
            <h2>{{ stats.pending }}</h2>
          </div>
        </div>
      </div>
    </div>

    <router-link
      to="/doctor/appointments"
      class="btn btn-outline-primary mt-3"
    >
      View Appointments
    </router-link>

    <div v-if="error" class="alert alert-danger mt-3">
      {{ error }}
    </div>
  </div>
</template>

<script>
import api from '../../api/axios'

export default {
  name: 'DoctorDashboard',
  data() {
    return {
      stats: {
        total_appointments: 0,
        completed: 0,
        pending: 0
      },
      error: null
    }
  },
  async mounted() {
    try {
      const res = await api.get('/doctor/dashboard')
      this.stats = res.data
    } catch {
      this.error = 'Failed to load dashboard'
    }
  }
}
</script>
