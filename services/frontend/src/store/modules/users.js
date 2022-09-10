import axios from 'axios';

const state = {
  user: null,
};

const getters = {
  isAuthenticated: state => !!state.user,
  stateUser: state => state.user,
};

const actions = {
  async register({dispatch}, form) {
    await axios.post('register', form);
    let UserForm = new FormData();
    UserForm.append('username', form.username);
    UserForm.append('password', form.password);
    await dispatch('logIn', UserForm);
  },
  async logIn({dispatch}, user) {
    try{
      let response = await axios.post('login', user);
      await dispatch('viewMe'); 

      if(response.status != 200){
        console.log("login fail");
        return false;
      }
    }
    catch(err){
      console.log("login fail, caught error, returning false");
      return false;
    }
   
    return true;
  },
  async viewMe({commit}) {
    let {data} = await axios.get('users/whoami');
    await commit('setUser', data);
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteUser({}, id) {
    await axios.delete(`user/${id}`);
  },
  async logOut({commit}) {
    let user = null;
    commit('logout', user);
  }
};

const mutations = {
  setUser(state, username) {
    state.user = username;
  },
  logout(state, user){
    state.user = user;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};
