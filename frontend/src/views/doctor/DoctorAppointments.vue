<template>
  <div class="container mt-4">
    <h3 class="mb-3">My Appointments</h3>

    <table class="table table-bordered">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>Patient</th>
          <th>Date</th>
          <th>Time</th>
          <th>Status</th>
          <th style="width: 260px">Actions</th>
        </tr>
      </thead>

      <tbody v-if="appointments.length">
        <tr v-for="(a, i) in appointments" :key="a.appointment_id">
          <td>{{ i + 1 }}</td>

          <td>
            {{ a.patient_name }}<br />
            <small class="text-muted">ID: {{ a.patient_id }}</small>
          </td>

          <td>{{ a.date }}</td>
          <td>{{ a.time }}</td>

          <td>
            <span class="badge" :class="statusClass(a.status)">
              {{ a.status }}
            </span>
          </td>

          <td>
            <!-- History -->
            <button
              class="btn btn-sm btn-outline-info me-2"
              @click="viewHistory(a.patient_id)"
            >
              History
            </button>

            <!-- Add Treatment -->
            <button
              v-if="a.status === 'Booked'"
              class="btn btn-sm btn-primary me-2"
              @click="openTreatment(a)"
            >
              Add Treatment
            </button>

            <!-- Edit Treatment -->
            <button
              v-if="a.status === 'Completed' && a.has_treatment"
              class="btn btn-sm btn-warning"
              @click="openTreatment(a)"
            >
              Edit Treatment
            </button>
          </td>
        </tr>
      </tbody>

      <tbody v-else>
        <tr>
          <td colspan="6" class="text-center text-muted">
            No appointments found
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Treatment Modal -->
    <AddTreatment
      v-if="selectedAppointment"
      :appointment="selectedAppointment"
      @close="selectedAppointment = null"
      @saved="onTreatmentSaved"
    />
  </div>
</template>

<script>
import api from '../../api/axios'
import AddTreatment from './AddTreatment.vue'

export default {
  name: 'DoctorAppointments',
  components: { AddTreatment },

  data() {
    return {
      appointments: [],
      selectedAppointment: null
    }
  },

  methods: {
    statusClass(status) {
      return {
        'bg-success': status === 'Completed',
        'bg-warning': status === 'Booked',
        'bg-danger': status === 'Cancelled'
      }
    },

    async loadAppointments() {
      try {
        const res = await api.get('/doctor/appointments')
        this.appointments = res.data
      } catch (err) {
        alert('Failed to load appointments')
        console.error(err)
      }
    },

    openTreatment(appointment) {
      this.selectedAppointment = appointment
    },

    onTreatmentSaved() {
      this.selectedAppointment = null
      this.loadAppointments()
    },

    viewHistory(patientId) {
      if (!patientId) {
        alert('Patient ID missing')
        return
      }
      this.$router.push(`/doctor/patients/${patientId}/history`)
    }
  },

  mounted() {
    this.loadAppointments()
  }
}
</script>
