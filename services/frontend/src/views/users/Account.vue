<template>
  <section>
    <h2>Account</h2>
    <hr/><br/>

    <div v-if="user">
      <p><strong>{{ $t('full_name') }}:</strong> <span>{{ user.full_name }}</span></p>
      <p><strong>{{ $t('email') }}:</strong> <span>{{ user.username }}</span></p>
      <p><strong>{{ $t('account_role') }}:</strong> 
        <span v-if="user.role"> {{ user.role.label }} </span>
        <span v-if="!user.role"> {{ $t('new_user_role') }} </span>
      </p>
      <p><button @click="deleteAccount()" 
        id="remove_account_btn" class="btn btn-danger">{{ $t('delete_account') }}
      </button></p>
    </div>
  </section>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
export default {
  name: 'Account',
  created: function() {
    return this.$store.dispatch('viewMe');
  },
  computed: {
    ...mapGetters({user: 'stateUser' }),
  },
  methods: {
    ...mapActions(['deleteUser']),
    async deleteAccount() {
      try {
        await this.deleteUser(this.user.id);
        await this.$store.dispatch('logOut');
        this.$router.push('/');
      } catch (error) {
        console.error(error);
      }
    }
  },
}
</script>

<style>
#remove_account_btn{
  float: right;
}
</style>
