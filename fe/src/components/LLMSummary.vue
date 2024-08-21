<script setup>
import {defineProps, onMounted, ref} from "vue";

const props = defineProps({
  lectureCode: String
})

const summary = ref("")
const showSpinner = ref(false);
onMounted(() => {
  showSpinner.value = true;
  console.log("request llm lectureCode: " + props.lectureCode)
  summary.value = await fetch("http://localhost:8000/llm/" + props.lectureCode)
      .then((response) => {
        showSpinner.value = false;
        response.json()["summary"];
      }).catch(error => console.log(error))
})


</script>

<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  <div v-if="showSpinner === true"></div>
  <div class="spinner-border" role="status"></div>
  <div id="llm-summary-container">
    <div style="white-space: pre-wrap;">
      {{summary}}
    </div>
  </div>
</template>

<style scoped>

</style>