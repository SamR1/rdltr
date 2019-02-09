<template>
  <header id="header">
    <div class="logo">
      <router-link to="/">
        rdltr <small>a simple "read-it later" app</small>
      </router-link>
    </div>
    <nav id="responsive-navbar" class="nav" @click="displayMenu">
      <ul>
        <li v-if="!auth" class="menu">
          <router-link to="/register">Register</router-link>
        </li>
        <li v-if="!auth" class="menu">
          <router-link to="/login">Log in</router-link>
        </li>
        <li v-if="auth" class="user menu">
          <router-link to="/profile">{{ username }}</router-link>
        </li>
        <li v-if="auth" class="menu">
          <router-link to="/settings">Settings</router-link>
        </li>
        <li v-if="auth" class="menu">
          <span @click="onLogout" class="logout">Logout</span>
        </li>
      </ul>
    </nav>
    <div @click="displayMenu" id="nav-icon">
      <i class="fa fa-bars"></i>
    </div>
  </header>
</template>

<script>
export default {
  computed: {
    auth() {
      return this.$store.getters.isAuthenticated
    },
    username() {
      return this.$store.getters.user.username
    },
  },
  methods: {
    onLogout() {
      this.$store.dispatch('logout')
    },
    displayMenu() {
      let x = document.getElementById('responsive-navbar')
      if (x.className === 'nav') {
        x.className += ' responsive'
      } else {
        x.className = 'nav'
      }
    },
  },
}
</script>

<style scoped>
#header {
  height: 56px;
  display: flex;
  flex-flow: row;
  justify-content: space-between;
  align-items: center;
  background-color: #8c95aa;
  padding: 0 20px;
}

#nav-icon {
  color: white;
  display: none;
}

.logo {
  font-weight: bold;
  color: white;
}

.logo a {
  text-decoration: none;
  color: white;
}

nav {
  height: 100%;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
  height: 100%;
  display: flex;
  flex-flow: row;
  align-items: center;
}

li {
  margin: 0 16px;
}

li a {
  text-decoration: none;
  color: white;
}

li a:hover,
li a:active,
li a.router-link-active {
  color: #c7dce1;
}

.logout {
  background-color: transparent;
  border: none;
  font: inherit;
  color: white;
  cursor: pointer;
}

.user {
  color: white;
}

@media screen and (max-width: 767.98px) {
  #responsive-navbar {
    z-index: 1;
  }
  #responsive-navbar ul {
    display: none;
  }
  #nav-icon {
    float: right;
    display: block;
  }

  #responsive-navbar.responsive {
    background-color: #f4f5f7;
    height: auto;
    left: 0;
    position: absolute;
    top: 56px;
    width: 100%;
  }

  #responsive-navbar.responsive ul {
    float: none;
    display: block;
    text-align: left;
  }

  #responsive-navbar.responsive li {
    padding: 20px;
  }

  #responsive-navbar.responsive li a,
  #responsive-navbar.responsive li span {
    color: #4e4e4e;
  }

  #responsive-navbar.responsive li a:hover,
  #responsive-navbar.responsive li span:hover {
    color: #778487;
  }
}
</style>
