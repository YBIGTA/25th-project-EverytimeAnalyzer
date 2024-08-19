<script setup>
import {sample_lecture_list} from "@/sample_data";
console.log(sample_lecture_list);
</script>

<template>
  <div class="container">
    <div v-for="lecture in sample_lecture_list" :key="lecture.name" class="lectureBoard">
      <p> {{lecture.name }}</p>
      <p> {{lecture.code }}</p>
      <p> {{lecture.professorList }}</p>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
}

.lectureBoard {
  margin: 10px 20px;
}
</style>