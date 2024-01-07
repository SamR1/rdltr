<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { reactive, toRefs } from 'vue'
import { useRoute } from 'vue-router'

import type { ILoginRegisterFormData, ILoginRegisterPayload } from '@/types'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'

interface Props {
  actionType: string
}

const props = defineProps<Props>()
const { actionType } = toRefs(props)

const appStore = useAppStore()
const { errorMessage } = storeToRefs(appStore)
const userStore = useUserStore()

const route = useRoute()

const formData: ILoginRegisterFormData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

function onSubmit(actionType: string) {
  const payload: ILoginRegisterPayload = {
    email: formData.email,
    password: formData.password
  }
  if (actionType === 'register') {
    payload.username = formData.username
    payload.password_conf = formData.confirmPassword
  }
  const redirect_url = route.query.from ? route.query.from.toString() : null
  userStore.loginOrRegister(payload, actionType, redirect_url)
}
</script>

<template>
  <div id="actionType" class="contnr">
    <div class="rdltr-box">
      <form @submit.prevent="onSubmit(actionType)">
        <div v-if="actionType === 'register'" class="input">
          <label for="username">Username</label>
          <input id="username" required v-model="formData.username" />
        </div>
        <div class="input">
          <label for="email">Email</label>
          <input id="email" required type="email" v-model="formData.email" />
        </div>
        <div class="input">
          <label for="password">Password</label>
          <input
            id="password"
            required
            type="password"
            v-model="formData.password"
          />
        </div>
        <div v-if="actionType === 'register'" class="input">
          <label for="confirm-password">Confirm Password</label>
          <input
            id="confirm-password"
            type="password"
            required
            v-model="formData.confirmPassword"
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

<style scoped lang="scss"></style>
