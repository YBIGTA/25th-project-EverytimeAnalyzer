<script setup>
import LectureTable from "@/components/LectureTable.vue";
import SearchBar from "@/components/SearchBar.vue";
import ReviewList from "@/components/ReivewList.vue";

const host = "http://localhost:8000"
const sampleLectureCode = "UCE1105-01-00"
</script>

<template>
  <SearchBar/>
  <LectureTable/>
  <div class="review-table">
    <ReviewList :host="host" :path="'/reviews/'+sampleLectureCode"/>
  </div>
</template>

<style>
.review-table {
  display: flex;
}
</style>
