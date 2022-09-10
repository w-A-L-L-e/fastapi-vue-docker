import Vue from 'vue';
import VueRouter from 'vue-router';

import store from '@/store';
import Home from '@/views/Home.vue';

import AccessDenied from '@/views/AccessDenied';

import UnconfiguredUser from '@/views/users/UnconfiguredUser';
import ManageUsers from '@/views/users/ManageUsers';
import Login from '@/views/users/Login';
import Account from '@/views/users/Account';
import Register from '@/views/users/Register';

import Notes from '@/views/notes/Notes';
import EditNote from '@/views/notes/EditNote';
import Note from '@/views/notes/Note';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: "Home",
    component: Home,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/notes',
    name: 'Notes',
    component: Notes,
    meta: {requiresAuth: true, allowedRoles: ['admin']},
  },
  {
    path: '/note/:id',
    name: 'Note',
    component: Note,
    meta: {requiresAuth: true},
    props: true,
  },
  {
    path: '/editnote/:id',
    name: 'EditNote',
    component: EditNote,
    meta: {requiresAuth: true, allowedRoles: ['admin']},
    props: true,
  },
  {
    path: '/users',
    name: 'Registered users',
    component: ManageUsers,
    meta: {requiresAuth: true, allowedRoles: ['admin']},
  },
  {
    path: '/account',
    name: 'Account',
    component: Account,
    meta: {requiresAuth: true},
  },
  {
    path: '/unconfigured_user',
    name: 'Account nog niet aktief',
    component: UnconfiguredUser,
    meta: {requiresAuth: true},
  },
  {
    path: '/access_denied',
    name: 'Geen toegang',
    component: AccessDenied,
    meta: {requiresAuth: true},
  },
  {
      path: "/:catchAll(.*)",
      redirect: '/'
      // catch all redirects to home page, we can also do this and show a 404 error page:
      // name: "NotFound",
      // component: PageNotFound,
      // meta: {
      //   requiresAuth: false
      // }
  }
]

const router = new VueRouter({
  mode: 'history', // https://v3.router.vuejs.org/guide/essentials/history-mode.html 
  base: process.env.BASE_URL,
  routes,
});


router.beforeEach((to, from, next) => {
  let auth_required = false;
  let allowed_roles = [];

  if (to.matched.some(record => record.meta.requiresAuth)) {
    to.matched.some( (route) => {
      auth_required = route.meta.requiresAuth;
    })
  }
     
  if (to.matched.some(record => record.meta.allowedRoles)) {
    to.matched.some( (route) => {
      auth_required = true;
      allowed_roles = route.meta.allowedRoles;
    })
  }

  if(!auth_required){ 
    next();
    return;
  }

  // we check logged in, and possibly roles
  if(store.getters.isAuthenticated){
    if(allowed_roles && allowed_roles.length){
      console.log("allowed_roles=", allowed_roles);

      let user = store.getters.stateUser;
      if(user && user.role){
        if( allowed_roles.includes(user.role.role) ){
          console.log("access to role", user.role.role, "allowed");
          next();
          return;
        }
      }

      // if denied
      next('/access_denied');
      return;
    }
    else{ // all roles allowed
      next();
      return;
    }
  }

  // unauthenticated
  next('/login');
  return;
});

export default router;
