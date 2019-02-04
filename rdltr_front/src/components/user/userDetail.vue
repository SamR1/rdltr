<template>
  <div id=actionType class="contnr">
    <div class="user-form">
      <form>
        <div class="input">
          <label for="username">Username</label>
          <input
            id="username"
            disabled
            v-model="user.username">
        </div>
        <div class="input">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            disabled
            v-model="user.email">
        </div>
        <div class="input">
          <label for="email">Inscription date</label>
          <input
            id="creationDate"
            disabled
            v-model="user.created_at">
        </div>
        <div v-if="actionType === 'editProfile'" class="input">
          <label for="password">Old password</label>
          <input
            type="password"
            id="oldPassword"
            required
            v-model="oldPassword">
        </div>
        <div v-if="actionType === 'editProfile'" class="input">
          <label for="password">New password</label>
          <input
            type="password"
            id="password"
            required
            v-model="newPassword">
        </div>
        <div v-if="actionType === 'editProfile'" class="input">
          <label for="confirm-password">Confirm New Password</label>
          <input
            type="password"
            id="confirm-password"
            required
            v-model="confirmNewPassword">
        </div>
        <div v-if="actionType === 'editProfile'" class="submit">
          <button type="submit" @click.prevent="onSubmit()">Submit</button>
          <router-link to="/profile" tag="button" class="cancel">Cancel</router-link>
        </div>
        <div v-else class="submit">
          <router-link to="/profile/edit" tag="button">Change password</router-link>
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
      oldPassword: '',
      newPassword: '',
      confirmNewPassword: ''
    }
  },
  computed: {
    errMessage () {
      return this.$store.getters.userErrorMessage
    },
    user () {
      return this.$store.getters.user
    }
  },
  methods: {
    onSubmit () {
      const formData = {
        old_password: this.oldPassword,
        new_password: this.newPassword,
        new_password_conf: this.confirmNewPassword
      }
      this.$store.dispatch('updateProfile', formData).then(() => {
        this.oldPassword = ''
        this.newPassword = ''
        this.confirmNewPassword = ''
      })
    }
  }
}
</script>

<style scoped>
  .input input:disabled {
    background-color: inherit;
    border: None;
    color: #4e4e4e;
  }

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
