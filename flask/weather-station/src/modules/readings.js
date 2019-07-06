import axios from "axios";

const state = {
  temperatures: [],
  humiditys: [],
  temperaturechartdata: {},
  humiditychartdata: {}
};

const getters = {
  getTemperatures: state => state.temperatures,
  getHumiditys: state => state.humiditys,
  getTemperatureChartData: state => state.temperaturechartdata,
  getHumidityChartData: state => state.humiditychartdata
};

const actions = {
  async fetchTemperatures({ commit }) {
    await axios
      .get(`http://192.168.0.81:5000/getTemperatures`)
      .then(response => {
        commit("SET_TEMPERATURES", response.data);
        commit("SET_TEMPERATURECHART", response.data);
      })
      .catch(err => {
        console.log(err);
      });
  },
  async fetchHumiditys({ commit }) {
    await axios
      .get(`http://192.168.0.81:5000/getHumiditys`)
      .then(response => {
        commit("SET_HUMIDITYS", response.data);
        commit("SET_HUMIDITYCHARTDATA", response.data);
      })
      .catch(err => {
        console.log(err);
      });
  }
};

const mutations = {
  SET_TEMPERATURES: (state, temperatures) => {
    state.temperatures = temperatures;
  },
  SET_HUMIDITYS: (state, humiditys) => (state.humiditys = humiditys),
  SET_TEMPERATURECHART: (state, temperatures) => {
    var times = [];
    var values = [];
    temperatures.forEach(element => {
      var date = element.date.split(" ");
      var time = date[1].split(":");
      var t = time[0] + ":" + time[1];
      times.push(t);
      values.push(element.value);
    });
    const chart = {
      labels: times,
      datasets: [
        {
          label: "Temperature",
          backgroundColor: "rgba(71, 183,132,.5)",
          borderColor: "rgba(71, 183,132,1)",
          data: values
        }
      ]
    };
    state.temperaturechartdata = chart;
  },
  SET_HUMIDITYCHARTDATA: (state, humidity) => {
    var times = [];
    var values = [];
    humidity.forEach(element => {
      var date = element.date.split(" ");
      var time = date[1].split(":");
      var t = time[0] + ":" + time[1];
      times.push(t);
      values.push(element.value);
    });
    const chart = {
      labels: times,
      datasets: [
        {
          label: "Humidity",
          backgroundColor: "rgba(14,73,193,.5)",
          borderColor: "rgba(14,73,193,0.75)",
          data: values
        }
      ]
    };
    state.humiditychartdata = chart;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
