<template>
  <section>
    <h2>{{ $t('login_form_title') }}</h2>
    <hr/><br/>

    <form @submit.prevent="submit">
      <div v-show="login_error">
        <div class="alert alert-danger" role="alert">{{ $t('wrong_username_or_password') }}</div>
      </div>
      <div class="mb-3">
        <label for="username" class="form-label">{{ $t('login_user') }}:</label>
        <input type="text" name="username" v-model="form.username" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">{{ $t('login_password') }}:</label>
        <input type="password" name="password" v-model="form.password" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">{{ $t('login_button') }}</button>
    </form>
  </section>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password:'',
      },
      login_error: false
    };
  },
  methods: {
    ...mapActions(['logIn']),
    async submit() {
      const User = new FormData();
      User.append('username', this.form.username);
      User.append('password', this.form.password);

      let logged_in = await this.logIn(User);
      if(logged_in){
        let user = this.$store.getters.stateUser;

        if((!user.role)||(user.role.role == "unconfigured_user")){
          this.$router.push('/unconfigured_user');
          return;
        }

        if(user.role.role == "admin"){
          this.$router.push('/users');
          return;
        }
        if(user.role.role == "moderator"){
          this.$router.push('/account');
          return;
        }
      }
      else{
        console.log("login fail");
        this.login_error = true;
      }
    }
  }
}
</script>

<style>
</style>

