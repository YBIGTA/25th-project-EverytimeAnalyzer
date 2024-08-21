<script setup>
import {defineEmits, defineProps, ref} from 'vue'

const props = defineProps({
  host: String,
  path: String,
})

const emit = defineEmits(['getRecommendLectureCodes']);

const query = ref('')


//TODO: exception control
async function request() {
      console.log("query in component: ", query.value)
      let lectureCodeList = await fetch(props.host + props.path + "/?query=" + query.value)
            .then(response => response.json())

    lectureCodeList.value = lectureCodeList.sort((a, b) => b[1] - a[1])
    emit('getRecommendLectureCodes',
        lectureCodeList.map(item => item[0]),
        query.value
    )
}
</script>

<template>
  <div id="form-container">
    <div v-for="idx in 1" :key="idx">
      <div class="input-container">
        <label :v-for="'topic'+idx+'-form'">topic{{ idx }}</label>
        <input type="text" :id="'topic'+idx+'-form'" v-model="query">
      </div>
    </div>
    <button id="input-submit" @click="request"> submit</button>
  </div>

  <!--  </div>-->
</template>

<style scoped>
#form-container {
  width: 50%;
  border: 1px solid aqua;
}

#input-submit {
  border-radius: 12px;
  width: 100px;
  height: 30px;
  background-color: #303245;
  color: white;

  position: relative;
  left: 600px;
  top: 10px;

}

.input-container {
  height: 50px;
  width: 700px;
  margin-top: 10px;
  display: flex;
}

input {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
  padding: 4px 20px 0;
  border-radius: 12px;
  border: 0;
  background-color: #303245;
  color: #eee;
  font-size: 18px;
}

label {
  color: #65657b;
  font-size: 20px;
  line-height: 14px;

  position: relative;
  top: 20px;
  margin-right: 10px;
}

</style>