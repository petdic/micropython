import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

import readingsModule from "../src/modules/readings.js";

export default new Vuex.Store({
  modules: {
    readings: readingsModule
  },
  state: {},
  mutations: {},
  actions: {}
});
