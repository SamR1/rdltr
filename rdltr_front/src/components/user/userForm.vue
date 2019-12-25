<template>
  <div id="actionType" class="contnr">
    <div class="rdltr-box">
      <form @submit.prevent="onSubmit(actionType)">
        <div v-if="actionType === 'register'" class="input">
          <label for="username">Username</label>
          <input id="username" required v-model="username" />
        </div>
        <div class="input">
          <label for="email">Email</label>
          <input id="email" required type="email" v-model="email" />
        </div>
        <div class="input">
          <label for="password">Password</label>
          <input id="password" required type="password" v-model="password" />
        </div>
        <div v-if="actionType === 'register'" class="input">
          <label for="confirm-password">Confirm Password</label>
          <input
            id="confirm-password"
            type="password"
            required
            v-model="confirmPassword"
          />
        </div>
        <p v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </p>
        <div class="submit">
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: ['actionType'],
  data() {
    return {
      confirmPassword: '',
      email: '',
      password: '',
      username: '',
    }
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage
    },
  },
  watch: {
    $route() {
      this.$store.commit('setErrorMessage', null)
    },
  },
  beforeDestroy() {
    this.$store.commit('setErrorMessage', null)
  },
  methods: {
    onSubmit(actionType) {
      const formData = {
        email: this.email,
        password: this.password,
      }
      if (actionType === 'register') {
        formData.username = this.username
        formData.password_conf = this.confirmPassword
      }
      const redirect_url = this.$route.query.from
      return this.$store.dispatch('loginOrRegister', {
        actionType,
        formData,
        redirect_url,
      })
    },
  },
}
</script>

<style scoped></style>
