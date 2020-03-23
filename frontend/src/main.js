import Vue from 'vue'
import App from './App.vue'
import AudioRecorder from 'vue-audio-recorder'

Vue.config.productionTip = false;

Vue.use(AudioRecorder)

new Vue({
  render: h => h(App),
}).$mount('#app')
