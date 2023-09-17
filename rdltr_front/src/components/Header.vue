<script setup lang="ts">
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const { authUser } = storeToRefs(userStore)

function displayMenu() {
  let element = document.getElementById('responsive-navbar')
  if (element) {
    if (element.className === 'nav') {
      element.className += ' responsive'
    } else {
      element.className = 'nav'
    }
  }
}
function onLogout() {
  userStore.logout()
}
</script>

<template>
  <header id="header">
    <div class="logo">
      <router-link to="/">
        rdltr <small>a simple "read-it later" app</small>
      </router-link>
    </div>
    <nav id="responsive-navbar" class="nav" @click="displayMenu">
      <ul>
        <li v-if="!authUser" class="menu">
          <router-link to="/register">Register</router-link>
        </li>
        <li v-if="!authUser" class="menu">
          <router-link to="/login">Log in</router-link>
        </li>
        <li v-if="authUser" class="user menu">
          <router-link to="/profile">{{ authUser.username }}</router-link>
        </li>
        <li v-if="authUser" class="menu">
          <router-link to="/settings">Settings</router-link>
        </li>
        <li v-if="authUser" class="menu">
          <button @click="onLogout" class="logout">Logout</button>
        </li>
        <li v-if="authUser" class="menu">
          <router-link to="/articles/add" title="add a new article">
            <i class="fa fa-plus" aria-hidden="true" />
          </router-link>
        </li>
      </ul>
    </nav>
    <div @click="displayMenu" id="nav-icon" aria-label="menu">
      <i aria-hidden="true" class="fa fa-bars" />
    </div>
  </header>
</template>

<style scoped lang="scss">
#header {
  align-items: center;
  background-color: #8c95aa;
  display: flex;
  flex-flow: row;
  height: 56px;
  justify-content: space-between;
  padding: 0 20px;
}

#nav-icon {
  color: white;
  display: none;
}

.logo {
  color: white;
  font-weight: bold;
}

.logo a {
  color: white;
  text-decoration: none;
}

.logout {
  background-color: transparent;
  border: none;
  color: white;
  cursor: pointer;
  font: inherit;
}

.user {
  color: white;
}

nav {
  height: 100%;
}

ul {
  align-items: center;
  display: flex;
  flex-flow: row;
  height: 100%;
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  margin: 0 16px;
}

li a {
  color: white;
  text-decoration: none;
}

li a:hover,
li a:active,
li a.router-link-active {
  color: #c7dce1;
}

@media screen and (max-width: 767.98px) {
  #responsive-navbar {
    z-index: 1;
  }
  #responsive-navbar ul {
    display: none;
  }
  #nav-icon {
    display: block;
    float: right;
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
    display: block;
    float: none;
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

  .logout {
    color: #4e4e4e;
    padding: 0;
  }
}
</style>
