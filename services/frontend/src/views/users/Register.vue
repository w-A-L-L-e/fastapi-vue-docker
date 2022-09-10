<template>
  <section>
    <h2>{{ $t('register_form_title') }}</h2>
    <hr/><br/>

    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="username" class="form-label">{{ $t('register_form_username') }}:</label>
        <input type="text" name="username" v-model="user.username" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="full_name" class="form-label">{{ $t('register_form_full_name') }}:</label>
        <input type="text" name="full_name" v-model="user.full_name" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">{{ $t('register_form_password') }}:</label>
        <input type="password" name="password" v-model="user.password" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">{{ $t('register_form_button') }}</button>
    </form>
  </section>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  name: 'Register',
  data() {
    return {
      user: {
        username: '',
        full_name: '',
        password: '',
      },
    };
  },
  methods: {
    ...mapActions(['register']),
    async submit() {
      try {
        await this.register(this.user);
        // freshly registered is not configured yet (no role)
        this.$router.push('/unconfigured_user');
      } catch (error) {
        throw 'Username already exists. Please try again.';
      }
    },
  },
};
</script>
