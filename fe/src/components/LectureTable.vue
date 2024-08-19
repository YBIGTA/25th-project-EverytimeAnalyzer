<script setup>
import {onMounted, ref, defineProps} from "vue";

const props = defineProps({
  host: String,
  path: String,
})
const lectureInfo = ref({});

onMounted(async () => {
  lectureInfo.value = await fetch(props.host + props.path)
      .then(response => response.json())
  console.log(lectureInfo.value);
})

</script>

<template>
  <div class="container">
    <div>
      <div>{{lectureInfo.code}}</div>
      <div>{{lectureInfo.name}}</div>
    </div>
  </div>
</template>

<style scoped>
.container {
  box-sizing: border-box;
  display: flex;
  border: black solid 1px;
  width: 200px;
  height: 100px;
  padding: 10px;
  margin: 10px;
}

</style>