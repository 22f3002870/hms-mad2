<template>
  <div class="container mt-4">
    <h3>Patients</h3>

    <table class="table table-bordered mt-3">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Age</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="p in patients" :key="p.patient_id">
          <td>{{ p.patient_id }}</td>
          <td>{{ p.name }}</td>
          <td>{{ p.email }}</td>
          <td>{{ p.age }}</td>
        </tr>

        <tr v-if="patients.length === 0">
          <td colspan="4" class="text-center text-muted">
            No patients found
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '../../api/axios'

export default {
  name: 'AdminPatients',
  data() {
    return {
      patients: []
    }
  },
  async mounted() {
    const res = await api.get('/admin/patients')
    this.patients = res.data
  }
}
</script>
