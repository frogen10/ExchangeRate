import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      id: '',
      username: ''
    },
    isAuthenticated: false,
    token: '',
    client: {
      id: '',
      default_currency: '',
    }
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
        state.user.username = localStorage.getItem('username')
        state.user.id = localStorage.getItem('userid')
        state.client.id = localStorage.getItem('clientid')
        state.client.default_currency = localStorage.getItem('default_currency')
      } else {
        state.user.id = ''
        state.user.username = ''
        state.token = ''
        state.isAuthenticated = false
        state.client = {
          id: '',
          default_currency: ''
        }
      }
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state) {
      state.user.id = ''
      state.user.username = ''
      state.token = ''
      state.isAuthenticated = false
      state.client = {
        id: '',
        default_currency: ''
      }
    },
    setUser(state, user) {
      state.user = user
    },
    setClient(state, client) {
      state.client = client
    }
  },
  actions: {
  },
  modules: {
  }
})
