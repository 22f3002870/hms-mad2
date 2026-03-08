<template>
  <div class="container mt-4">
    <h3 class="mb-3">Manage Doctors</h3>

    <table class="table table-bordered table-hover">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Email</th>
          <th>Department</th>
          <th>Available</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(doctor, index) in doctors" :key="doctor.doctor_id">
          <td>{{ index + 1 }}</td>
          <td>{{ doctor.name }}</td>
          <td>{{ doctor.email }}</td>
          <td>{{ doctor.department || '—' }}</td>
          <td>
            <span
              class="badge"
              :class="doctor.is_available ? 'bg-success' : 'bg-danger'"
            >
              {{ doctor.is_available ? 'Yes' : 'No' }}
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
import { getDoctors } from '../../api/admin'

export default {
  name: 'ManageDoctors',
  data() {
    return {
      doctors: [],
      error: null
    }
  },
  async mounted() {
    try {
      const res = await getDoctors()
      this.doctors = res.data
    } catch (err) {
      this.error =
        err.response?.data?.error ||
        'Failed to load doctors'
    }
  }
}
</script>
