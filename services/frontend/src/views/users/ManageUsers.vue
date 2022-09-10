<template>
  <div>

    <h2>{{ $t('user_management_title') }}</h2>
    <hr/>

    <div v-show="save_success">
        <div class="alert alert-success" role="alert">{{save_success}}</div>
    </div>
    <div v-show="save_error">
        <div class="alert alert-danger" role="alert">{{save_error}}</div>
    </div>
    <div v-show="!save_error && !save_success" class="alert-spacer"></div>

    <section>
      <table class="table table-hover table-bordered">
        <thead>
          <tr class="table-secondary">
            <th>{{ $t('user_management_name') }}</th>
            <th>{{ $t('user_management_email') }}</th>
            <th>{{ $t('user_management_account_type') }}</th>
            <th>&nbsp;</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{user.full_name}}</td>
            <td>{{user.username}}</td>
            <td v-if="user.role">
              <!-- {{user.role.label}} -->
              <select name="user_role" 
              v-model="user.role" 
              class="form-select" aria-label="Selecteer">
                <option v-for="role in user_roles" :value="role" :key="role.id">
                  {{role.label}}
                </option>
              </select>
            </td>
            <td>
              <button
                class="btn btn-secondary btn-sm"
                @click="saveRole(user)">
                  {{ $t('user_management_save_btn') }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ManageUsers',
  data() {
    return {
      save_success: '',
      save_error: '',
      users: [],
      user_roles: []
    };
  },
  created: function() {

    axios.get('/roles').then((response)=>{
        this.user_roles = response.data;
      }).catch( (error) => {
        console.log("caught error fetching user_roles = ", error);
    });

    axios.get('/users').then((response)=>{
      for(let i in response.data){
        let user = response.data[i];
        if(!user.role){
          user.role = {
            id: 1,
            label: "not set"
          }
        }
      }
      this.users = response.data;
    }).catch( (error) => {
      console.log("caught error while fetching user list=", error);
    });
  },
  methods: {

    errorAlert(msg){
      this.save_error = msg;
      setTimeout(()=>{this.save_error=''}, 3000);
    },
    successAlert(msg){
      this.save_success = msg;
      setTimeout(()=>{this.save_success=''}, 3000);
    },

    async saveRole(user){
      let role_id = 1;
      if(user.role) role_id = user.role.id;
      axios.patch(
        "/users/"+user.id+"/update_role", 
        {role_id: role_id}
      ).then((response)=>{
        console.log("role saved, response=", response);
        this.successAlert("Rol voor gebruiker "+user.username+" is aangepast");
        user=response.data;
      }).catch( (error) => {
        console.log("error during saving of role", error)
      });
    }

  },
};

</script>

<style>
.alert-spacer {
  height: 3.5em;
}
.alert {
  height: 2.5em;
  padding: 8px 10px;
  animation-name: FadeIn;
  animation-duration: 0.5s;
  transition-timing-function: linear;
}
@keyframes FadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>

