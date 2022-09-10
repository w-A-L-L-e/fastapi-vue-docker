<template>
  <section>
    <h2>{{ $t('home_page_title') }}</h2>
    <hr/><br/>

    <p>{{ $t('home_page_content') }}</p>

    <div v-if="isLoggedIn" id="logout">
      You are now logged in
    </div>

    <div v-else>
      <p>
        <span><a href="/register">{{ $t('register') }}</a></span>
        <span> {{ $t('or') }} </span>
        <span><a href="/login">{{ $t('login') }}</a></span>
      </p>
    </div>

  </section>
</template>

<script>
export default {
  name: 'Home',
  components: {},
  mounted(){
  },
  computed : {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    }
  },
}
</script>
