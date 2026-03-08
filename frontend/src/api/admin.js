import api from './axios'

export const getAdminDashboard = () =>
  api.get('/admin/dashboard')

export const getDoctors = () =>
  api.get('/admin/doctors')


export const createDoctor = data =>
  api.post('/admin/doctors', data)

export const getDepartments = () =>
  api.get('/admin/departments')



export const createDepartment = (data) =>
  api.post('/admin/departments', data)
