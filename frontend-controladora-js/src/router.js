import { createWebHistory, createRouter } from "vue-router";

const routes =  [
  {
    path: "/",
    alias: "/login",
    name: "login",
    component: () => import("./components/Login")
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("./components/Dashboard"),
    meta: {
      requiresAuth: true // Add meta field to indicate protected route
    }
  },
  {
    path: "/backups",
    name: "backups",
    component: () => import("./components/BackupsList"),
    meta: {
      requiresAuth: true // Add meta field to indicate protected route
    }
  },
  {
    path: "/backups/:id",
    name: "backups-details",
    component: () => import("./components/Backup"),
    meta: {
      requiresAuth: true // Add meta field to indicate protected route
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = sessionStorage.getItem('token');
    if (token) {
      // User is authenticated, proceed to the route
      next();
    } else {
      // User is not authenticated, redirect to login
      next('/login');
    }
  } else {
    // Non-protected route, allow access
    next();
  }
});


export default router;
