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
    </div>
  </div>
</template>

<script>
import api from '../../api/defaultApi'

export default {
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    onSubmit () {
      const formData = {
        email: this.email,
        password: this.password
      }
      console.log(formData)
      const path = '/auth/login'
      console.log('test login')
      api.post(path, formData)
        .then(res => console.log(res))
        .catch(err => console.error(err))
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

  .input {
    margin: 10px auto;
  }

  .input label {
    display: block;
    color: #4e4e4e;
    margin-bottom: 6px;
  }

  .input input {
    font: inherit;
    width: 100%;
    padding: 6px 12px;
    box-sizing: border-box;
    border: 1px solid #ccc;
  }

  .input input:focus {
    outline: none;
    border: 1px solid #8c95aa;
    background-color: #eee;
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
