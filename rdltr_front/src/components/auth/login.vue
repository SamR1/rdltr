<template>
  <div id="login">
    <div class="login-form">
      <form @submit.prevent="onSubmit">
        <div class="input">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email">
        </div>
        <div class="input">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password">
        </div>
        <div class="submit">
          <button type="submit">Submit</button>
        </div>
      </form>
      <p v-if="errMessage" class="user-error">{{ errMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      email: '',
      password: ''
    }
  },
  computed: {
    errMessage () {
      return this.$store.getters.userErrorMessage
    }
  },
  methods: {
    onSubmit () {
      const formData = {
        email: this.email,
        password: this.password
      }
      return this.$store.dispatch('loginOrRegister', { actionType: 'login', formData })
    }
  }
}
</script>

<style scoped>
  .login-form {
    width: 400px;
    margin: 30px auto;
    border: 1px solid #eee;
    padding: 20px;
    box-shadow: 0 2px 3px #ccc;
  }

  .user-error {
    color: red;
    text-align: center;
  }
</style>
