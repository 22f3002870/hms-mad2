import Vue from "vue";
import Router from "vue-router";
import store from "../store";

Vue.use(Router);

const router = new Router({
  mode: "history",

  routes: [
    { path: "/", redirect: "/login" },

    {
      path: "/login",
      component: () => import("../views/auth/Login.vue")
    },

    // ---------------- ADMIN ----------------

    {
      path: "/admin",
      component: () => import("../views/admin/AdminDashboard.vue"),
      meta: { role: "admin" }
    },

    {
      path: "/admin/doctors",
      component: () => import("../views/admin/ManageDoctors.vue"),
      meta: { role: "admin" }
    },

    {
      path: "/admin/doctors/add",
      component: () => import("../views/admin/AddDoctor.vue"),
      meta: { role: "admin" }
    },

    {
      path: "/admin/departments",
      component: () => import("../views/admin/AdminDepartments.vue"),
      meta: { role: "admin" }
    },

    {
      path: "/admin/departments/add",
      component: () => import("../views/admin/AddDepartment.vue"),
      meta: { role: "admin" }
    },

    {
      path: "/admin/patients",
      component: () => import("../views/admin/ManagePatients.vue"),
      meta: { role: "admin" }
    },

    {
      path: "/admin/appointments",
      component: () => import("../views/admin/AdminAppointments.vue"),
      meta: { role: "admin" }
    },

    // ---------------- DOCTOR ----------------

    {
      path: "/doctor",
      component: () => import("../views/doctor/DoctorDashboard.vue"),
      meta: { role: "doctor" }
    },

    {
      path: "/doctor/appointments",
      component: () => import("../views/doctor/DoctorAppointments.vue"),
      meta: { role: "doctor" }
    },

    {
      path: "/doctor/appointments/:id/treatment",
      component: () => import("../views/doctor/AddTreatment.vue"),
      meta: { role: "doctor" }
    },

    {
      path: "/doctor/patients/:patientId/history",
      component: () => import("../views/doctor/PatientHistory.vue"),
      meta: { role: "doctor" }
    },

    // ---------------- PATIENT ----------------

    {
      path: "/patient",
      component: () => import("../views/patient/PatientDashboard.vue"),
      meta: { role: "patient" }
    },

    {
      path: "/patient/book",
      component: () => import("../views/patient/BookAppointment.vue"),
      meta: { role: "patient" }
    },

    {
      path: "/patient/history",
      component: () => import("../views/patient/TreatmentHistory.vue"),
      meta: { role: "patient" }
    },

    {
      path: "/register",
      component: () => import("../views/auth/Register.vue")
    },
    {
    path:'/patient/profile',
    component:()=>import('../views/patient/EditProfile.vue'),
    meta:{role:'patient'}
    }


  ]
});

router.beforeEach((to, from, next) => {
  const role = store.state.auth.role;
  const isLoggedIn = !!role;

  if (to.path === "/login" || to.path === "/register") {
    next();
    return;
  }

  if (to.meta.role) {
    if (!isLoggedIn) {
      next("/login");
      return;
    }

    if (to.meta.role !== role) {
      next("/login");
      return;
    }
  }

  next();
});

export default router;

