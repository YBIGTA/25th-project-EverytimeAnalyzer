<script setup>
import {reactive, ref} from 'vue'
import LectureTable from "@/components/LectureTable.vue";
import SearchBar from "@/components/SearchBar.vue";
import ReviewList from "@/components/ReivewList.vue";
// import LLMSummary from "@/components/LLMSummary.vue";
const host = "http://localhost:8000"
// const sampleLectureCode = "UCE1105-01-00"

const lectureCodes = reactive({codes: []})
const reviewIdx = ref(-1)
const query = ref("")

function getRecommendLectureCodes(codes, qquery) {
  lectureCodes.codes = codes
  query.value =  qquery
  console.log("query: ", query.value)
}
</script>

<template>
 <div id="top-container">
   <div class="lecture-container">
     <article>
       <SearchBar
           :host="host"
           path="/model"
           @getRecommendLectureCodes="getRecommendLectureCodes"/>
       <!--      <div v-if="0 <= reviewIdx">-->
       <!--        <LLMSummary-->
       <!--            :lectureCode="lectureCodes.codes[reviewIdx]"-->
       <!--            :key="reviewIdx"-->
       <!--        />-->
       <!--      </div>-->
     </article>
     <article :key="lectureCodes.codes">
       <div class="lecture-table">
         <div v-for="(lectureCode, idx) in lectureCodes.codes" :key="idx">
           <LectureTable :host="host"
                         :path="'/lecture/'+lectureCode"
                         :lectureCode="lectureCode"
                         :query="query"
                         @click="reviewIdx=idx"
           />
         </div>
       </div>
       <div class="review-table">
         <div v-if="0 <= reviewIdx">
           <ReviewList :host="host"
                       :path="'/reviews/'+lectureCodes.codes[reviewIdx]"
                       :key="reviewIdx"
           />
         </div>
       </div>
     </article>
   </div>
 </div>
</template>

<style>
#top-container {
  width: 100%;
  border: 5px solid pink;
  display: flex;
  justify-content: center;
}
.lecture-container {
  width: 1200px;
  border: 5px solid aqua;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;

}
article {
  width: 900;
  border: 5px solid green;
  margin-bottom: 30px;
}

article .lecture-table {
  display: flex;
}

article .review-table {
  border: 1px solid chocolate;
}
</style>
