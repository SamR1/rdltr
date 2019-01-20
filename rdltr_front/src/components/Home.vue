<template>
  <div>
    <p>Home page</p>
    <p>Ping backend: {{ apiPing }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      apiPing: ''
    }
  },
  methods: {
    getRandomFromBackend () {
      const path = `http://localhost:5000/api/ping`
      axios.get(path)
        .then(response => {
          this.apiPing = response.data.message
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.getRandomFromBackend()
  }
}
</script>
