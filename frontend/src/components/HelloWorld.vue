<template>
	<div>
		<audio-recorder
		format="wav"
		filename="file.wav"
		class="audio-recorder"
		:after-recording="callback"
		:attempts="3"
		:time="2"/>
		<h1 v-if="responces.length">Output: </h1>
		<div v-if="responces.length" class="responces-wrapper">
			<div class=responce v-for="responce in responces" :key="responce">
				{{ responce }}
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data: function () {
    return {
      responces: []
    }
  },
  methods: {
    async callback (data) {
		console.log(data);
		var form = new FormData();
		form.append("file", data.blob);
		var resp = await axios.post("http://localhost:5000/getText", form).catch(rep => console.log(rep));
		console.log(resp.data);
		this.responces.unshift(resp.data);
    },
  }
}
</script>
<style>
.audio-recorder {
	margin: 0 auto;
}

h1 {
	text-align: center;
}

.responces-wrapper {
	white-space: pre-line;
	width: 900px;
	background: rgba(220, 220, 220, 0.3);
	margin: 0 auto;
	border-radius: 20px;
	padding: 20px

}

.responce {
	color: #90EE90;
}
</style>
