<template>
<div class="container mt-4">

<h2 class="mb-4">Patient Dashboard</h2>

<div class="row">

<!-- BOOK APPOINTMENT -->
<div class="col-md-3">
<div class="card bg-primary text-white mb-3">
<div class="card-body text-center">

<h5>Book Appointment</h5>

<router-link
to="/patient/book"
class="btn btn-light mt-2"
>
Book Now
</router-link>

</div>
</div>
</div>

<!-- VIEW HISTORY -->
<div class="col-md-3">
<div class="card bg-success text-white mb-3">
<div class="card-body text-center">

<h5>View Treatment History</h5>

<router-link
to="/patient/history"
class="btn btn-light mt-2"
>
View History
</router-link>

</div>
</div>
</div>

<!-- EXPORT CSV -->
<div class="col-md-3">
<div class="card bg-dark text-white mb-3">
<div class="card-body text-center">

<h5>Export Treatments CSV</h5>

<button
class="btn btn-light mt-2"
@click="exportCSV"
>
Download CSV
</button>

</div>
</div>
</div>

<!-- EDIT PROFILE -->
<div class="col-md-3">
<div class="card bg-info text-white mb-3">
<div class="card-body text-center">

<h5>Edit Profile</h5>

<router-link
to="/patient/profile"
class="btn btn-light mt-2"
>
Edit Profile
</router-link>

</div>
</div>
</div>

</div>

</div>
</template>

<script>

import api from "@/api/axios"

export default {

name: "PatientDashboard",

methods: {

async exportCSV() {

try {

// Trigger celery export job
await api.post("/patient/export")

alert("CSV export started. Preparing download...")

// Wait a little for celery to generate file
setTimeout(async () => {

const response = await api.get(
"/patient/export/download",
{ responseType: "blob" }
)

const url = window.URL.createObjectURL(
new Blob([response.data])
)

const link = document.createElement("a")

link.href = url
link.setAttribute("download", "treatment_history.csv")

document.body.appendChild(link)

link.click()

link.remove()

}, 2000)

} catch (err) {

alert("Export failed")

}

}

}

}

</script>