<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>ExchangeRate</strong></router-link>
      </div>

      <div class="navbar-menu">
        <div class="navbar-end">
          <router-link :to="{name:'About'}" class="navbar-item">About</router-link>
          <router-link :to="{name:'Calculator'}" class="navbar-item">Calculator</router-link>
          <template v-if="$store.state.isAuthenticated">
            <router-link :to="{name:'Dashboard'}" class="navbar-item">Dashboard</router-link>
            <div class="navbar-item">
              <div class="buttons">
                <router-link :to="{name:'MyAccount'}" class="button is-light">My account</router-link>
              </div>
            </div>      
          </template>

          <template v-else>
            <router-link to="/" class="navbar-item">Home</router-link>

            <div class="navbar-item">
              <div class="buttons">
                <router-link :to="{name:'SignUp'}" class="button is-success"><strong>Sign up</strong></router-link>
                <router-link :to="{name:'LogIn'}" class="button is-light">Log in</router-link>
              </div>
            </div> 
          </template>
        </div>
      </div>
    </nav>

    <section class="section">
      <router-view/>
    </section>

    <footer class="footer">
      <p class="has-text-centered">Copyright (c) 2024</p>
    </footer>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'App',
    beforeCreate() {
      this.$store.commit('initializeStore')

      const token = this.$store.state.token

      if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
      } else {
        axios.defaults.headers.common['Authorization'] = ""
      }
    }
  }
</script>

<style lang="scss">
@import '../node_modules/bulma/';
</style>
