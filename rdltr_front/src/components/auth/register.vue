<template>
  <div id="register">
    <div class="register-form">
      <form @submit.prevent="onSubmit">
        <div class="input">
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
        <div class="input">
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
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    onSubmit () {
      const formData = {
        username: this.username,
        email: this.email,
        password: this.password,
        password_conf: this.confirmPassword
      }
      console.log(formData)
      const path = '/auth/register'
      console.log('test register')
      axios.post(path, formData)
        .then(res => console.log(res))
        .catch(err => console.log(err))
    }
  }
}
</script>

<style scoped>
  .register-form {
    width: 400px;
    margin: 30px auto;
    border: 1px solid #eee;
    padding: 20px;
    box-shadow: 0 2px 3px #ccc;
  }

  .input {
    margin: 10px auto;
  }

  .input label {
    display: block;
    color: #4e4e4e;
    margin-bottom: 6px;
  }

  .input.inline label {
    display: inline;
  }

  .input input {
    font: inherit;
    width: 100%;
    padding: 6px 12px;
    box-sizing: border-box;
    border: 1px solid #ccc;
  }

  .input.inline input {
    width: auto;
  }

  .input input:focus {
    outline: none;
    border: 1px solid #8c95aa;
    background-color: #eee;
  }

  .input select {
    border: 1px solid #ccc;
    font: inherit;
  }

  .submit button {
    border: 1px solid #8c95aa;
    color: #8c95aa;
    padding: 10px 20px;
    font: inherit;
    cursor: pointer;
  }

  .submit button:hover,
  .submit button:active {
    background-color: #8c95aa;
    color: white;
  }

  .submit button[disabled],
  .submit button[disabled]:hover,
  .submit button[disabled]:active {
    border: 1px solid #ccc;
    background-color: transparent;
    color: #ccc;
    cursor: not-allowed;
  }
</style>
