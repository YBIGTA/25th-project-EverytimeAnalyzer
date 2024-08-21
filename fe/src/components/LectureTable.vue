<script setup>
import {onMounted, ref, defineProps} from "vue";

const props = defineProps({
  host: String,
  path: String,
  lectureCode: String,
  query: String,
})
const lectureInfo = ref({});
const topicDistanceList = ref([])


async function requestLectureInfo() {
  lectureInfo.value = await fetch(props.host + props.path)
      .then(response => response.json())
}
async function requestTopicDistanceList() {
  console.log("requesting " +"http://localhost:8000/model/sims/" + props.lectureCode + "/?query=" + props.query )
  topicDistanceList.value = await fetch("http://localhost:8000/model/sims/" + props.lectureCode + "/?query=" + props.query )
      .then(response => response.json())
}

onMounted(() => {
  requestLectureInfo()
  requestTopicDistanceList()
  console.log("topicDistanceList: ", topicDistanceList.value)
})

</script>

<template>
  <div class="lecture-container">
    <div>
      <div>{{lectureInfo.code}}</div>
      <div>{{lectureInfo.name}}</div>
      <br>
      <br>
      <div v-for="(value, key) in topicDistanceList" :key="key">
        <div> {{ key }}: {{ value }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.lecture-container {
  box-sizing: border-box;
  display: flex;
  border: black solid 1px;
  width: 170px;
  height: 200px;
  padding: 10px;
  margin: 10px;
}

</style>