import api from './axios'

export function getDoctors() {
  return api.get('/patient/doctors')
}

export function bookAppointment(data) {
  return api.post('/patient/appointments', data)
}
