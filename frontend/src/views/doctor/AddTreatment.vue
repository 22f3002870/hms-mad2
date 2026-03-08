<template>
  <div class="modal-backdrop-custom">
    <div class="modal-card">
      <h5 class="mb-3">
        {{ mode === 'edit' ? 'Edit Treatment' : 'Add Treatment' }}
      </h5>

      <form @submit.prevent="submitTreatment">
        <!-- Diagnosis -->
        <div class="mb-3">
          <label class="form-label">Diagnosis</label>
          <textarea
            class="form-control"
            v-model="form.diagnosis"
            required
          ></textarea>
        </div>

        <!-- Prescription -->
        <div class="mb-3">
          <label class="form-label">Prescription</label>
          <textarea
            class="form-control"
            v-model="form.prescription"
            required
          ></textarea>
        </div>

        <!-- Notes -->
        <div class="mb-3">
          <label class="form-label">Notes</label>
          <textarea
            class="form-control"
            v-model="form.notes"
          ></textarea>
        </div>

        <!-- Error -->
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <!-- Actions -->
        <div class="d-flex justify-content-end gap-2">
          <button
            type="button"
            class="btn btn-secondary"
            @click="$emit('close')"
            :disabled="loading"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="btn btn-success"
            :disabled="loading"
          >
            {{ loading ? 'Saving...' : 'Save Treatment' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../../api/axios'

export default {
  name: 'AddTreatment',

  props: {
    appointment: {
      type: Object,
      required: true
    },
    mode: {
      type: String,
      default: 'add' // 'add' | 'edit'
    }
  },

  data() {
    return {
      form: {
        diagnosis: '',
        prescription: '',
        notes: ''
      },
      loading: false,
      error: null
    }
  },

  mounted() {
    // Prefill form in EDIT mode
    if (this.mode === 'edit') {
      this.form.diagnosis = this.appointment.diagnosis || ''
      this.form.prescription = this.appointment.prescription || ''
      this.form.notes = this.appointment.notes || ''
    }
  },

  methods: {
    async submitTreatment() {
      this.loading = true
      this.error = null

      try {
        const url = `/doctor/appointments/${this.appointment.appointment_id}/treatment`

        if (this.mode === 'edit') {
          // 🔄 UPDATE (PUT)
          await api.put(url, this.form)
        } else {
          // ➕ CREATE (POST)
          await api.post(url, this.form)
        }

        this.$emit('saved')
      } catch (err) {
        console.error(err)
        this.error =
          err.response?.data?.error || 'Failed to save treatment'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.modal-backdrop-custom {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-card {
  background: #fff;
  padding: 20px;
  width: 500px;
  border-radius: 6px;
}
</style>
