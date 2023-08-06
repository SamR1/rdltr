<script setup lang="ts">
import { RouterView } from 'vue-router'

import Header from './components/Header.vue'
</script>

<template>
  <Header />
  <RouterView />
</template>

<style src="vue-multiselect/dist/vue-multiselect.css" />

<style lang="scss">
@import './scss/base.scss';
</style>
