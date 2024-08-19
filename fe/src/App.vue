<script setup>
import { reactive } from 'vue'
import LectureTable from "@/components/LectureTable.vue";
import SearchBar from "@/components/SearchBar.vue";
import ReviewList from "@/components/ReivewList.vue";

const host = "http://localhost:8000"
const sampleLectureCode = "UCE1105-01-00"

const lectureCodes = reactive({codes: ["foo1", "foo2", "foo3"]})

function getRecommendLectureCodes(codes) {
  lectureCodes.codes = codes
}
</script>

<template>
  <SearchBar @getRecommendLectureCodes="getRecommendLectureCodes"/>

  <div class="lecture-table">
    <LectureTable :host="host" :path="'/lecture/'+sampleLectureCode"/>
    <LectureTable :host="host" :path="'/lecture/'+sampleLectureCode"/>
    <LectureTable :host="host" :path="'/lecture/'+sampleLectureCode"/>
  </div>

  <div class="review-table">
    <ReviewList :host="host" :path="'/reviews/'+sampleLectureCode"/>
  </div>
</template>

<style>
.review-table {
  display: flex;
}

.lecture-table {
  display: flex;
}
</style>
