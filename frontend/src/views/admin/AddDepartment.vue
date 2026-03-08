<template>
  <div class="container mt-4">
    <h3 class="mb-3">Add Department</h3>

    <form @submit.prevent="submitDepartment" class="card p-4">

      <div class="mb-3">
        <label class="form-label">Department Name</label>
        <input
          type="text"
          class="form-control"
          v-model="form.name"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Description (optional)</label>
        <textarea
          class="form-control"
          rows="3"
          v-model="form.description"
        ></textarea>
      </div>

      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <div v-if="success" class="alert alert-success">
        Department created successfully
      </div>

      <button
        type="submit"
        class="btn btn-primary"
        :disabled="loading"
      >
        {{ loading ? 'Adding...' : 'Add Department' }}
      </button>

    </form>
  </div>
</template>

<script>
import { createDepartment } from '../../api/admin'

export default {
  name: 'AddDepartment',

  data() {
    return {
      form: {
        name: '',
        description: ''
      },
      error: null,
      success: false,
      loading: false
    }
  },

  methods: {
    async submitDepartment() {
      this.error = null
      this.success = false
      this.loading = true

      try {
        await createDepartment(this.form)
        this.success = true

        this.form = {
          name: '',
          description: ''
        }

        // Optional redirect:
        // this.$router.push('/admin/departments')

      } catch (err) {
        this.error =
          err.response?.data?.error ||
          'Failed to create department'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>


