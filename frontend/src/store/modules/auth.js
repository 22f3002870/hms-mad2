import { login, logoutUser } from '../../api/auth'

export default {
  namespaced: true,

  state: {
    role: localStorage.getItem('role'),
    token: localStorage.getItem('token')
  },

  mutations: {
    SET_AUTH(state, payload) {
      state.role = payload.role
      state.token = payload.token

      // 🔐 Persist login
      localStorage.setItem('role', payload.role)
      localStorage.setItem('token', payload.token)
    },

    LOGOUT(state) {
      state.role = null
      state.token = null

      // 🔐 Clear storage
      localStorage.removeItem('role')
      localStorage.removeItem('token')
    }
  },

  actions: {
    async login({ commit }, data) {
      const res = await login(data)
      commit('SET_AUTH', res.data)
    },

    async logout({ commit }) {
      await logoutUser()
      commit('LOGOUT')
    }
  }
}
