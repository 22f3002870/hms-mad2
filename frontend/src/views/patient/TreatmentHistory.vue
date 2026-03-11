<template>

<div class="container mt-4">

<h3 class="mb-3">Treatment History</h3>

<table class="table table-bordered">

<thead class="table-dark">
<tr>
<th>#</th>
<th>Status</th>
<th>Date</th>
<th>Time</th>
<th>Diagnosis</th>
<th>Prescription</th>
<th>Notes</th>
<th style="width:220px">Actions</th>
</tr>
</thead>

<tbody>

<tr v-for="(h,i) in history" :key="h.appointment_id">

<td>{{ i + 1 }}</td>

<td>
<span
:class="{
'badge bg-warning': h.status==='Booked',
'badge bg-success': h.status==='Completed',
'badge bg-danger': h.status==='Cancelled'
}"
>
{{ h.status }}
</span>
</td>

<td>{{ h.date || '-' }}</td>

<td>{{ h.time || '-' }}</td>

<td>{{ h.diagnosis || '-' }}</td>

<td>{{ h.prescription || '-' }}</td>

<td>{{ h.notes || '-' }}</td>

<td>

<!-- CANCEL -->
<button
v-if="h.status==='Booked'"
class="btn btn-danger btn-sm me-2"
@click="cancelAppointment(h.appointment_id)"
>
Cancel
</button>

<!-- RESCHEDULE -->
<button
v-if="h.status==='Booked'"
class="btn btn-warning btn-sm"
@click="openReschedule(h.appointment_id)"
>
Reschedule
</button>

<span v-if="h.status!=='Booked'">-</span>

</td>

</tr>

<tr v-if="history.length===0">
<td colspan="8" class="text-center text-muted">
No history found
</td>
</tr>

</tbody>

</table>


<!-- RESCHEDULE PANEL -->

<div v-if="showReschedule" class="card mt-4 p-3">

<h5 class="mb-3">Reschedule Appointment</h5>

<div class="row">

<div class="col-md-4">

<label class="form-label">New Date</label>

<input
type="date"
class="form-control"
v-model="newDate"
:min="today"
/>

</div>

<div class="col-md-4">

<label class="form-label">New Time</label>

<input
type="time"
class="form-control"
v-model="newTime"
/>

</div>

<div class="col-md-4 d-flex align-items-end">

<button
class="btn btn-primary me-2"
@click="confirmReschedule"
>
Update
</button>

<button
class="btn btn-secondary"
@click="cancelReschedule"
>
Cancel
</button>

</div>

</div>

</div>

</div>

</template>


<script>

import api from '@/api/axios'

export default{

data(){
return{
history:[],
showReschedule:false,
selectedAppointment:null,
newDate:"",
newTime:"",
today:new Date().toISOString().split('T')[0]
}
},

methods:{

async fetchHistory(){

try{

const res = await api.get('/patient/history')

this.history = res.data

}catch{

alert("Failed to load history")

}

},

async cancelAppointment(id){

if(!confirm("Cancel this appointment?")) return

try{

await api.put(`/patient/appointments/${id}/cancel`)

alert("Appointment cancelled successfully")

this.fetchHistory()

}catch{

alert("Cancel failed")

}

},

openReschedule(id){

this.selectedAppointment = id

this.showReschedule = true

this.newDate = ""

this.newTime = ""

},

cancelReschedule(){

this.showReschedule = false

},

async confirmReschedule(){

if(!this.newDate || !this.newTime){

alert("Please select date and time")

return

}

try{

await api.put(`/patient/appointments/${this.selectedAppointment}/reschedule`,{
date:this.newDate,
time:this.newTime
})

alert("Appointment rescheduled successfully")

this.showReschedule = false

this.fetchHistory()

}catch(err){

alert(err.response?.data?.error || "Reschedule failed")

}

}

},

mounted(){

this.fetchHistory()

}

}

</script>