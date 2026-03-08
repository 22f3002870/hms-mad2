<template>
  <div class="container mt-4">
    <h3 class="mb-4">Book Appointment</h3>

    <form @submit.prevent="bookAppointment">

      <!-- Doctor Selection -->
      <div class="mb-3">
        <label class="form-label">Select Doctor</label>
        <select
          class="form-select"
          v-model="form.doctor_id"
          required
        >
          <option disabled value="">Select Doctor</option>

          <option
            v-for="d in doctors"
            :key="d.doctor_id"
            :value="d.doctor_id"
          >
            {{ d.doctor_name }}
            | {{ d.department_name }}
            | {{ d.department_description }}
            | {{ d.is_available ? 'Available' : 'Not Available' }}
          </option>
        </select>
      </div>

      <!-- Date -->
      <div class="mb-3">
        <label class="form-label">Date</label>
        <input
          type="date"
          class="form-control"
          v-model="form.date"
          required
        />
      </div>

      <!-- Time -->
      <div class="mb-3">
        <label class="form-label">Time</label>
        <input
          type="time"
          class="form-control"
          v-model="form.time"
          required
        />
      </div>

      <!-- Error -->
      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <!-- Success -->
      <div v-if="success" class="alert alert-success">
        Appointment booked successfully
      </div>

      <button type="submit" class="btn btn-success">
        Book Appointment
      </button>

    </form>
  </div>
</template>

<script>
import api from '@/api/axios'

export default {
  name: 'BookAppointmentView',

  data() {
    return {
      doctors: [],
      form: {
        doctor_id: '',
        date: '',
        time: ''
      },
      error: null,
      success: false
    }
  },

  async mounted() {
    try {
      const res = await api.get('/patient/doctors')
      this.doctors = res.data
    } catch (err) {
      this.error = 'Failed to load doctors'
    }
  },

  methods: {
    async bookAppointment() {
      this.error = null
      this.success = false

      try {
        await api.post('/patient/appointments', this.form)
        this.success = true

        // reset form
        this.form = {
          doctor_id: '',
          date: '',
          time: ''
        }
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          'Failed to book appointment'
      }
    }
  }
}
</script>
