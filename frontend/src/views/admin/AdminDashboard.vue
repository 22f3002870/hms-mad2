<template>
  <div class="container mt-4">
    <h2 class="mb-4">Admin Dashboard</h2>

    <!-- Stats Cards -->
    <div class="row">
      <div class="col-md-4">
        <div class="card text-white bg-primary mb-3">
          <div class="card-body text-center">
            <h5 class="card-title">Doctors</h5>
            <h2>{{ dashboard.total_doctors }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card text-white bg-success mb-3">
          <div class="card-body text-center">
            <h5 class="card-title">Patients</h5>
            <h2>{{ dashboard.total_patients }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card text-white bg-dark mb-3">
          <div class="card-body text-center">
            <h5 class="card-title">Appointments</h5>
            <h2>{{ dashboard.total_appointments }}</h2>
          </div>
        </div>
      </div>
    </div>

    <!-- Admin Actions -->
    <div class="mt-5">
      <h5 class="mb-3">Admin Actions</h5>

      <div class="d-flex flex-wrap gap-2">

        <!-- Department Management -->
        <router-link
          to="/admin/departments"
          class="btn btn-outline-secondary"
        >
          View Departments
        </router-link>

        <router-link
          to="/admin/departments/add"
          class="btn btn-secondary"
        >
          Add Department
        </router-link>

        <!-- Doctor Management -->
        <router-link
          to="/admin/doctors"
          class="btn btn-outline-primary"
        >
          View Doctors
        </router-link>

        <router-link
          to="/admin/doctors/add"
          class="btn btn-primary"
        >
          Add Doctor
        </router-link>

        <!-- Others -->
        <router-link
          to="/admin/patients"
          class="btn btn-outline-success"
        >
          View Patients
        </router-link>

        <router-link
          to="/admin/appointments"
          class="btn btn-outline-dark"
        >
          View Appointments
        </router-link>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-danger mt-3">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { getAdminDashboard } from '../../api/admin'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      dashboard: {
        total_doctors: 0,
        total_patients: 0,
        total_appointments: 0
      },
      error: null
    }
  },
  async mounted() {
    try {
      const res = await getAdminDashboard()
      this.dashboard = res.data
    } catch (err) {
      this.error =
        err.response?.data?.error ||
        'Failed to load dashboard data'
    }
  }
}
</script>
