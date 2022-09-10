<template>
  <section>
    <h2>{{ $t('unconfigured_page_title') }}</h2>

    <p> {{ $t('unconfigured_page_content') }}</p>

  </section>
</template>
<script>

export default {
  name: 'UnconfiguredUser',
  //computed : {
  //  isLoggedIn: function() {
  //    return this.$store.getters.isAuthenticated;
  //  }
  //},
}
</script>
