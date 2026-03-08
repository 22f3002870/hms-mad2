
import api from './axios'

export const getDoctorDashboard = () =>
  api.get('/api/doctor/dashboard')

export const getDoctorAppointments = () =>
  api.get('/api/doctor/appointments')
