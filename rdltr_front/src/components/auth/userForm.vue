<template>
  <div id=actionType>
    <div class="user-form">
      <form @submit.prevent="onSubmit(actionType)">
        <div v-if="actionType === 'register'" class="input">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username">
        </div>
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
        <div v-if="actionType === 'register'" class="input">
          <label for="confirm-password">Confirm Password</label>
          <input
            type="password"
            id="confirm-password"
            v-model="confirmPassword">
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
  props: ['actionType'],
  data () {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  },
  computed: {
    errMessage () {
      return this.$store.getters.userErrorMessage
    }
  },
  methods: {
    onSubmit (actionType) {
      const formData = {
        email: this.email,
        password: this.password
      }
      if (actionType === 'register') {
        formData.username = this.username
        formData.password_conf = this.confirmPassword
      }
      return this.$store.dispatch('loginOrRegister', { actionType, formData })
    }
  }
}
</script>

<style scoped>
  .user-form {
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
