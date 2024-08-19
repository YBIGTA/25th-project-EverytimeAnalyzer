<script setup>
import LectureTable from "@/components/LectureTable.vue";
import SearchBar from "@/components/SearchBar.vue";
import ReviewList from "@/components/ReivewList.vue";
</script>

<template>
<!--  <img alt="Vue logo" src="./assets/logo.png">-->
  <SearchBar/>
  <LectureTable/>
  <div class="review-table">
    <ReviewList/>
  </div>
</template>

<style>
.review-table{
  display: flex;
}
</style>
