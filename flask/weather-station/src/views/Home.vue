<template>
  <div class="home">
    <h1 class="pt-2">Weather Station</h1>
    <img alt="Vue logo" src="../assets/logo.png">
    <div class="row d-flex justify-content-center">
      <div class="col-6 small p-3">
        <h3>Temperature: {{this.temperature}}</h3>
        <Chart :chart-data="getTemperatureChartData"></Chart>
      </div>
      <div class="col-6 small p-3">
        <h3>Humidity: {{this.humidity}}</h3>
        <Chart :chart-data="getHumidityChartData"></Chart>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import Chart from "@/components/Chart.vue";

import { mapActions, mapGetters } from "vuex";

export default {
  name: "home",

  components: {
    HelloWorld,
    Chart
  },
  data() {
    return {
      temperature: "",
      humidity: "",
      datacollection: null
    };
  },
  methods: {
    ...mapActions({
      fetchTemperatures: "readings/fetchTemperatures",
      fetchHumiditys: "readings/fetchHumiditys"
    })
  },
  computed: {
    ...mapGetters({
      getTemperatures: "readings/getTemperatures",
      getHumiditys: "readings/getHumiditys",
      getTemperatureChartData: "readings/getTemperatureChartData",
      getHumidityChartData: "readings/getHumidityChartData"
    })
  },
  sockets: {
    // connect: function() {
    //   console.log("socket connected");
    // },
    // mqtt_message: data => {
    //   var payload = data.payload.split(",");
    //   var t = payload[0];
    //   console.log(t);
    //   this.setTemperature("");
    //   this.humidity = payload[1];
    // }
  },
  created() {
    // $socket is socket.io-client instance
    this.fetchTemperatures();
    this.fetchHumiditys();

    const data = { topic: "temp_humidity" };
    this.$socket.emit("subscribe", JSON.stringify(data));
    this.sockets.subscribe("mqtt_message", data => {
      var payload = data.payload.split(",");
      var t = payload[0];
      var h = payload[1];
      this.temperature = t;
      this.humidity = h;
    });
  },
  mounted() {}
};
</script>
<style scoped>
.small {
  max-width: 450px;
  /* margin: auto; */
  margin-top: 15px;
}
</style>
