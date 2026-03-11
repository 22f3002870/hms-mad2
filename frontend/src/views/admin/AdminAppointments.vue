<template>
  <div class="container mt-4">
    <h3 class="mb-3">All Appointments</h3>

    <table class="table table-bordered table-striped">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>Doctor</th>
          <th>Department</th>
          <th>Patient</th>
          <th>Date</th>
          <th>Time</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        <tr v-if="appointments.length === 0">
          <td colspan="7" class="text-center">
            No appointments found
          </td>
        </tr>

        <tr
          v-for="(a, index) in appointments"
          :key="a.appointment_id"
        >
          <td>{{ index + 1 }}</td>
          <td>{{ a.doctor_name }}</td>
          <td>{{ a.department_name || '-' }}</td>
          <td>{{ a.patient_name }}</td>
          <td>{{ a.date }}</td>
          <td>{{ a.time }}</td>
          <td>
            <span
              class="badge"
              :class="{
                'bg-success': a.status === 'Completed',
                'bg-warning': a.status === 'Booked',
                'bg-danger': a.status === 'Cancelled'
              }"
            >
              {{ a.status }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
  </div>
</template>

<script>
import api from '@/api/axios'

export default {
  name: 'AdminAppointments',
  data() {
    return {
      appointments: [],
      error: null
    }
  },
  async mounted() {
    try {
      const res = await api.get('/admin/appointments')
      this.appointments = res.data
    } catch (err) {
      this.error = 'Failed to load appointments'
    }
  }
}
</script>
