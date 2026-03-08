<template>
  <div class="container mt-4">
    <h3 class="mb-3">Patient History</h3>

    <table class="table table-bordered">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>Date</th>
          <th>Status</th>
          <th>Diagnosis</th>
          <th>Prescription</th>
          <th>Notes</th>
        </tr>
      </thead>

      <tbody v-if="history.length">
        <tr v-for="(h, i) in history" :key="h.treatment_id">
          <td>{{ i + 1 }}</td>
          <td>{{ h.date }}</td>
          <td>{{ h.status }}</td>
          <td>{{ h.diagnosis }}</td>
          <td>{{ h.prescription }}</td>
          <td>{{ h.notes }}</td>
        </tr>
      </tbody>

      <tbody v-else>
        <tr>
          <td colspan="6" class="text-center text-muted">
            No history found
          </td>
        </tr>
      </tbody>
    </table>

    <button class="btn btn-secondary mt-3" @click="$router.back()">
      ← Back
    </button>
  </div>
</template>

<script>
import api from '../../api/axios'

export default {
  name: 'PatientHistory',

  data() {
    return {
      history: []
    }
  },

  async mounted() {
    const patientId = this.$route.params.patientId
    console.log('Loading history for patientId:', patientId)

    if (!patientId) {
      alert('Invalid patient ID')
      return
    }

    try {
      const res = await api.get(
        `/doctor/patients/${patientId}/history`
      )
      this.history = res.data
    } catch (err) {
      alert('Failed to load patient history')
      console.error(err)
    }
  }
}
</script>
