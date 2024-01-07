<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { reactive, toRefs } from 'vue'
import { useRouter } from 'vue-router'

import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'
import type { IUpdatePasswordFormData } from '@/types'

interface Props {
  actionType: string
}
const props = defineProps<Props>()
const { actionType } = toRefs(props)

const userStore = useUserStore()
const { authUser } = storeToRefs(userStore)
const appStore = useAppStore()
const { errorMessage } = storeToRefs(appStore)

const router = useRouter()

const formData: IUpdatePasswordFormData = reactive({
  oldPassword: '',
  newPassword: '',
  confirmNewPassword: ''
})

function emptyForm() {
  formData.oldPassword = ''
  formData.newPassword = ''
  formData.confirmNewPassword = ''
}
function onSubmit() {
  userStore.updatePassword(formData).then(() => {
    emptyForm()
  })
}
function onCancel() {
  emptyForm()
  router.push('/profile')
}
</script>

<template>
  <div class="rdltr-box" v-if="authUser">
    <form>
      <div class="input">
        <label for="username">Username</label>
        <input id="username" disabled v-model="authUser.username" />
      </div>
      <div class="input">
        <label for="email">Email</label>
        <input id="email" disabled type="email" v-model="authUser.email" />
      </div>
      <div class="input">
        <label for="creationDate">Inscription date</label>
        <input id="creationDate" disabled v-model="authUser.created_at" />
      </div>
      <div v-if="actionType === 'edit'" class="input">
        <label for="oldPassword">Old password</label>
        <input
          id="oldPassword"
          required
          type="password"
          v-model="formData.oldPassword"
        />
      </div>
      <div v-if="actionType === 'edit'" class="input">
        <label for="password">New password</label>
        <input
          id="password"
          required
          type="password"
          v-model="formData.newPassword"
        />
      </div>
      <div v-if="actionType === 'edit'" class="input">
        <label for="confirm-password">Confirm New Password</label>
        <input
          id="confirm-password"
          required
          type="password"
          v-model="formData.confirmNewPassword"
        />
      </div>
      <div class="submit" v-if="actionType === 'edit'">
        <button type="submit" @click.prevent="onSubmit()">Submit</button>
        <button type="submit" @click.prevent="onCancel()">Cancel</button>
      </div>
      <div v-else class="submit">
        <button type="submit" @click.prevent="$router.push('/profile/edit')">
          Change password
        </button>
      </div>
    </form>
    <p v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </p>
  </div>
</template>

<style scoped lang="scss">
.input input:disabled {
  background-color: inherit;
  border: None;
  color: #4e4e4e;
}
.submit button {
  margin-right: 0.5em;
}
</style>
