<script setup>
import {defineProps, onMounted, ref} from "vue";

const props = defineProps({
  lectureCode: String
})

const summary = ref("")
onMounted(async () => {
  console.log("request llm lectureCode: " + props.lectureCode)
  summary.value = await fetch("http://localhost:8000/llm/" + props.lectureCode)
      .then(response => response.json())
      .then(resp => resp["summary"])
      // .then(resp => resp["summary"].replace(/\n/g,'<br>'))
})

</script>

<template>
  <div id="llm-summary-container">
    <div style="white-space: pre-wrap;">
      {{summary}}
    </div>
  </div>
</template>

<style scoped>

</style>