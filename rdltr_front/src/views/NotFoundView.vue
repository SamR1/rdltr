<script setup lang="ts">
import router from '@/router'
</script>

<template>
  <div class="not-found">
    <div class="test">
      <p>Page not found!</p>
      <button class="btn-rdltr" @click="router.push('/')">Back to home</button>
    </div>
  </div>
</template>
