<template>
  <div id="actionType" class="contnr">
    <div class="rdltr-box">
      <form>
        <div class="input">
          <label for="username">Username</label>
          <input id="username" disabled v-model="user.username" />
        </div>
        <div class="input">
          <label for="email">Email</label>
          <input id="email" disabled type="email" v-model="user.email" />
        </div>
        <div class="input">
          <label for="email">Inscription date</label>
          <input id="creationDate" disabled v-model="user.created_at" />
        </div>
        <div v-if="actionType === 'editProfile'" class="input">
          <label for="password">Old password</label>
          <input
            id="oldPassword"
            required
            type="password"
            v-model="oldPassword"
          />
        </div>
        <div v-if="actionType === 'editProfile'" class="input">
          <label for="password">New password</label>
          <input id="password" required type="password" v-model="newPassword" />
        </div>
        <div v-if="actionType === 'editProfile'" class="input">
          <label for="confirm-password">Confirm New Password</label>
          <input
            id="confirm-password"
            required
            type="password"
            v-model="confirmNewPassword"
          />
        </div>
        <div class="submit" v-if="actionType === 'editProfile'">
          <button type="submit" @click.prevent="onSubmit()">Submit</button>
          <router-link class="cancel" tag="button" to="/profile"
            >Cancel</router-link
          >
        </div>
        <div v-else class="submit">
          <router-link tag="button" to="/profile/edit">
            Change password
          </router-link>
        </div>
      </form>
      <p v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: ['actionType'],
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      confirmNewPassword: '',
    }
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    user() {
      return this.$store.getters.user
    },
  },
  methods: {
    onSubmit() {
      const formData = {
        old_password: this.oldPassword,
        new_password: this.newPassword,
        new_password_conf: this.confirmNewPassword,
      }
      this.$store.dispatch('updateProfile', formData).then(() => {
        this.oldPassword = ''
        this.newPassword = ''
        this.confirmNewPassword = ''
      })
    },
  },
}
</script>

<style scoped>
.input input:disabled {
  background-color: inherit;
  border: None;
  color: #4e4e4e;
}
</style>
