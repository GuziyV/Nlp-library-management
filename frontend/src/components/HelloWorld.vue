<template>
		<div class="app">
			<div class="order">
				{{ selectedOrder }}
			</div>
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

const orders = {
	ORDER_SAY_COMMAND: "Please tell me what to do!",
	ORDER_SAY_NAME_OF_THE_BOOK: "Please tell name of the book",
	ORDER_FILL_INPUT: "Please feel the input below and pres send",
}

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
		command: "",
		selectedOrder: orders.ORDER_SAY_COMMAND,
		book: "",
    }
  },
  methods: {
	init() {
		this.textareaText = "",
		this.saidText = "",
		this.selectedOrder = orders.ORDER_SAY_COMMAND,
		this.book = "";
		this.textInputMode = false;
	},

    async callback(data) {
		console.log(data);
		if (this.selectedOrder === orders.ORDER_SAY_COMMAND) {
			await this.getCommandFromServer(data);
			this.selectedOrder = orders.ORDER_SAY_NAME_OF_THE_BOOK;
		} else if (this.selectedOrder === orders.ORDER_SAY_NAME_OF_THE_BOOK) {
			await this.getBookFromTheServer(data)
			if (this.command === "AddComment") {
				this.textInputMode = true;
			} else {
				this.sendCommandToServer();
				this.init();
			}
		}
	},

	async getCommandFromServer(data) {
		var form = new FormData();
		form.append("file", data.blob);
		var resp = await axios.post("http://localhost:5000/getCommand", form).catch(rep => console.log(rep));
		this.command = resp.data;
		this.responces.push("Your command is " + resp.data);
	},

	async sendCommandToServer() {
		if (this.command === "AddBook") {
			await this.sendNewBook();
		} else if (this.command === "RemoveBook") {
			await this.removeBook();
		}
	},

	async getBookFromTheServer(data) {
		var form = new FormData();
		form.append("file", data.blob);
		var resp = await axios.post("http://localhost:5000/getText", form).catch(rep => console.log(rep));
		this.book = resp.data;
		this.responces.push("Book: " + resp.data);
		this.book = resp.data;
	},

	async sendReviewText() {
		await axios.post("http://localhost:5000/sendReview", {
			review: this.textareaText,
			book: this.book,
		}).catch(rep => console.log(rep));
		this.textareaText = "";
		this.responces.push("Review was added");
		this.init();
	},

	async sendNewBook() {
		await axios.post("http://localhost:5000/addBook", {
			book: this.book,
		}).catch(rep => console.log(rep));
		this.textareaText = "";
		this.responces.push("Book was added");
		this.textInputMode = false;
	},

	async removeBook() {
		await axios.post("http://localhost:5000/removeBook", {
			book: this.book,
		}).catch(rep => console.log(rep));
		this.textareaText = "";
		this.responces.push("Book was removed");
		this.textInputMode = false;
	}
  }
}
</script>
<style>

.app {
	margin-bottom: 50px;
}

.order {
	font-style: italic;
	text-align: center;
	margin-bottom: 20px;
	font-size: 18px;
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
