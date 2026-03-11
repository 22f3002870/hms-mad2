```vue
<template>

<div class="container mt-4">

<div class="d-flex justify-content-between align-items-center mb-3">

<h3>Manage Doctors</h3>

<input
type="text"
class="form-control w-25"
placeholder="Search doctor or department..."
v-model="search"
@input="fetchDoctors"
/>

</div>

<table class="table table-bordered table-hover">

<thead class="table-dark">
<tr>
<th>#</th>
<th>Name</th>
<th>Email</th>
<th>Department</th>
<th>Available</th>
<th>Actions</th>
</tr>
</thead>

<tbody>

<tr v-for="(doctor,index) in doctors" :key="doctor.doctor_id">

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

<td>

<button
class="btn btn-danger btn-sm"
@click="deleteDoctor(doctor.doctor_id)"
>

Delete

</button>

</td>

</tr>

<tr v-if="doctors.length === 0">

<td colspan="6" class="text-center text-muted">

No doctors found

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

import api from "@/api/axios"

export default {

name: "ManageDoctors",

data(){

return{

doctors: [],
error: null,
search: ""

}

},

methods:{

async fetchDoctors(){

try{

const res = await api.get("/admin/doctors",{
params:{ search:this.search }
})

this.doctors = res.data

}catch(err){

this.error = err.response?.data?.error || "Failed to load doctors"

}

},

async deleteDoctor(id){

if(!confirm("Are you sure you want to delete this doctor?")) return

try{

await api.delete(`/admin/doctors/${id}`)

alert("Doctor deleted successfully")

this.fetchDoctors()

}catch(err){

alert(err.response?.data?.error || "Delete failed")

}

}

},

mounted(){

this.fetchDoctors()

}

}

</script>
```
