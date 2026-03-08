<template>
  <div class="container mt-4">
    <h3 class="mb-3">Add Doctor</h3>

    <form @submit.prevent="submitDoctor" class="card p-4">

      <div class="mb-3">
        <label class="form-label">Doctor Name</label>
        <input
          type="text"
          class="form-control"
          v-model="form.name"
          @input="success = false"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Email</label>
        <input
          type="email"
          class="form-control"
          v-model="form.email"
          @input="success = false"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Password</label>
        <input
          type="password"
          class="form-control"
          v-model="form.password"
          @input="success = false"
          required
        />
      </div>

      <!-- ✅ Department Dropdown -->
      <div class="mb-3">
        <label class="form-label">Department</label>
        <select
          class="form-select"
          v-model.number="form.department_id"
          required
        >
          <option disabled value="">
            Select Department
          </option>

          <option
            v-for="dept in departments"
            :key="dept.id"
            :value="dept.id"
          >
            {{ dept.name }}
          </option>
        </select>
      </div>

      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <div v-if="success" class="alert alert-success">
        Doctor created successfully
      </div>

      <button
        type="submit"
        class="btn btn-primary"
        :disabled="loading"
      >
        {{ loading ? 'Adding...' : 'Add Doctor' }}
      </button>

    </form>
  </div>
</template>

<script>
import { createDoctor, getDepartments } from '../../api/admin'

export default {
  name: 'AddDoctor',

  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        department_id: ''
      },
      departments: [],
      error: null,
      success: false,
      loading: false
    }
  },

  async mounted() {
    try {
      const res = await getDepartments()
      this.departments = res.data
    } catch (err) {
      this.error = 'Failed to load departments'
    }
  },

  methods: {
    async submitDoctor() {
      this.error = null
      this.success = false
      this.loading = true

      try {
        await createDoctor(this.form)
        this.success = true

        this.form = {
          name: '',
          email: '',
          password: '',
          department_id: ''
        }

        // Optional redirect after success:
        // this.$router.push('/admin/doctors')

      } catch (err) {
        this.error =
          err.response?.data?.error ||
          'Failed to create doctor'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
