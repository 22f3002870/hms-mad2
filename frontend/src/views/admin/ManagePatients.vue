<template>

<div class="container mt-4">

<div class="d-flex justify-content-between align-items-center mb-3">

<h3>Patients</h3>

<input
type="text"
class="form-control w-25"
placeholder="Search patient..."
v-model="search"
@input="fetchPatients"
/>

</div>

<table class="table table-bordered table-hover">

<thead class="table-dark">
<tr>
<th>ID</th>
<th>Name</th>
<th>Email</th>
<th>Age</th>
<th>Actions</th>
</tr>
</thead>

<tbody>

<tr v-for="patient in patients" :key="patient.patient_id">

<td>{{ patient.patient_id }}</td>
<td>{{ patient.name }}</td>
<td>{{ patient.email }}</td>
<td>{{ patient.age || '-' }}</td>

<td>
<button
class="btn btn-danger btn-sm"
@click="deletePatient(patient.patient_id)"
>
Delete
</button>
</td>

</tr>

<tr v-if="patients.length === 0">
<td colspan="5" class="text-center text-muted">
No patients found
</td>
</tr>

</tbody>

</table>

</div>

</template>

<script>

import api from "@/api/axios"

export default {

name:"ManagePatients",

data(){

return{

patients:[],
search:""

}

},

methods:{

async fetchPatients(){

try{

const res = await api.get("/admin/patients",{
params:{ search:this.search }
})

this.patients = res.data

}catch(err){

alert("Failed to load patients")

}

},

async deletePatient(id){

if(!confirm("Are you sure you want to delete this patient?")) return

try{

await api.delete(`/admin/patients/${id}`)

alert("Patient deleted successfully")

this.fetchPatients()

}catch(err){

alert(err.response?.data?.error || "Delete failed")

}

}

},

mounted(){

this.fetchPatients()

}

}

</script>