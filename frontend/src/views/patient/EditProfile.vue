<template>

<div class="container mt-4">

<h3 class="mb-4">Edit Profile</h3>

<form @submit.prevent="updateProfile">

<div class="mb-3">

<label class="form-label">Name</label>

<input
type="text"
class="form-control"
v-model="form.name"
required
/>

</div>

<div class="mb-3">

<label class="form-label">Email</label>

<input
type="email"
class="form-control"
v-model="form.email"
disabled
/>

</div>

<div class="mb-3">

<label class="form-label">Age</label>

<input
type="number"
class="form-control"
v-model="form.age"
/>

</div>

<button class="btn btn-primary">

Update Profile

</button>

</form>

</div>

</template>

<script>

import api from "@/api/axios"

export default {

name:"EditProfile",

data(){

return{

form:{
name:"",
email:"",
age:""
}

}

},

methods:{

async loadProfile(){

const res = await api.get("/patient/profile")

this.form = res.data

},

async updateProfile(){

try{

await api.put("/patient/profile",{
name:this.form.name,
age:this.form.age
})

alert("Profile updated successfully")

}catch(err){

alert("Update failed")

}

}

},

mounted(){

this.loadProfile()

}

}

</script>