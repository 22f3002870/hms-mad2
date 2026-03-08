<template>
  <div class="container mt-4">
    <h3 class="mb-3">Departments</h3>

    <table class="table table-bordered">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Description</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="(dept, index) in departments"
          :key="dept.id"
        >
          <td>{{ index + 1 }}</td>
          <td>{{ dept.name }}</td>
          <td>{{ dept.description || '-' }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { getDepartments } from '../../api/admin'

export default {
  name: 'AdminDepartments',

  data() {
    return {
      departments: [],
      error: null
    }
  },

  async mounted() {
    try {
      const res = await getDepartments()
      this.departments = res.data
    } catch (err) {
      this.error = 'Failed to load departments'
    }
  }
}
</script>
