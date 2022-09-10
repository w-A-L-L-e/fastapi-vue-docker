<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
      <div class="container">

        <a class="navbar-brand" href="/">{{ $t('app_brand_label') }}</a>

        <button class="navbar-toggler" type="button" 
          data-bs-toggle="collapse" data-bs-target="#navbarCollapse" 
          aria-controls="navbarCollapse" aria-expanded="false" 
          aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          
          <ul v-if="isLoggedIn" class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">{{ $t('menu_home') }}</router-link>
            </li>
            
            <template v-if="userRole != 'unconfigured_user'">
              <li v-if="userRole == 'admin'" class="nav-item">
                <router-link class="nav-link" to="/users">{{ $t('menu_gebruikers') }}</router-link>
              </li>
            </template>

            <li class="nav-item">
              <router-link class="nav-link" to="/account">{{ $t('menu_account') }}</router-link>
            </li>

            <li class="nav-item">
              <a class="nav-link" @click="logout">{{ $t('menu_logout') }}</a>
            </li>

            <li class="nav-item">
              <LocaleSwitcher/>
            </li>
          </ul>

          <ul v-else class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">{{ $t('menu_home') }}</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">{{ $t('menu_register') }}</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">{{ $t('menu_login') }}</router-link>
            </li>
            <li class="nav-item">
              <LocaleSwitcher/>
            </li>
          </ul>
        
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import LocaleSwitcher from "@/components/LocaleSwitcher"

export default {
  name: 'NavBar',
  components: {LocaleSwitcher},
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    },
    userRole: function() {
      let current_user = this.$store.getters.stateUser;
      if(!current_user.role) return "unconfigured_user";
      return current_user.role.role;
    }
  },
  methods: {
    async logout () {
      await this.$store.dispatch('logOut');

      // clear localstorage
      window.localStorage.clear()
      //setCookie('name', 'value', 0) deletes a cookie

      this.$router.push('/login');
    }
  },
}
</script>

<style scoped>
a {
  cursor: pointer;
}
.navbar {
  background-color: #114411 !important;
}
.navbar-nav{
  margin-left: auto;
  margin-right: -10px !important;
}
</style>
