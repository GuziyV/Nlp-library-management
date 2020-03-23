<template>
	<div class="hello">
		<audio-recorder
		class="audio-recorder"
		upload-url="YOUR_API_URL"
		:attempts="3"
		:time="2"
		:before-recording="callback"
		:pause-recording="callback"
		:after-recording="callback"
		:select-record="callback"
		:before-upload="callback"
		:successful-upload="callback"
		:failed-upload="callback"/>
	</div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  methods: {
    callback (data) {
		console.log(data.blob)
    }
  }
}
</script>
<style>
.audio-recorder {
	margin: 0 auto;
}
</style>
