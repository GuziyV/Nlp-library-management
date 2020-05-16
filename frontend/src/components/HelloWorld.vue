<template>
	<div class="app">
		<audio-recorder
		format="mp3"
		filename="file.mp3"
		class="audio-recorder"
		:bit-rate="192"
		:after-recording="callback"
		:attempts="3"
		:time="2"/>
		<h1 v-if="responces.length">Output: </h1>
		<div v-if="responces.length" class="responces-wrapper">
			<div class=responce v-for="responce in responces" :key="responce">
				{{ responce }}
			</div>
		</div>
		<div class="textarea-section" v-if="textInputMode">
			<textarea rows="6" v-model="textareaText" />
			<a class="send-review-btn" @click="sendReviewText">Send</a>
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
		responces: [],
		textareaText: "",
		saidText: "",
		textInputMode: false,
    }
  },
  methods: {
    async callback(data) {
		console.log(data);
		var form = new FormData();
		form.append("file", data.blob);
		var resp = await axios.post("http://localhost:5000/sendFile", form).catch(rep => console.log(rep));
		console.log(resp);
		if (resp.data.command === "AddComment") {
			// Ask for a review text
			this.saidText = resp.data.text;
			this.openTextInput();
		}
		else this.responces.unshift(resp.data);
	},
	openTextInput() {
		this.textInputMode = true;
	},
	async sendReviewText() {
		var resp = await axios.post("http://localhost:5000/sendReview", {
			review: this.textareaText,
			saidText: this.saidText,
		}).catch(rep => console.log(rep));
		this.textareaText = "";
		this.responces.unshift(resp.data);
		this.textInputMode = false;
	}
  }
}
</script>
<style>
.app {
	margin-bottom: 50px;
}
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

.textarea-section {
	width: 900px;
	margin: 0 auto;
	margin-top: 20px;
}

.textarea-section textarea {
	width: 100%;
}

.textarea-section .send-review-btn {
	float: right;
}

.send-review-btn {
	cursor: pointer;
	padding: 5px 10px;
	border: 1px solid black;
}
</style>
