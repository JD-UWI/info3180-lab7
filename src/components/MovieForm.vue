<template>
    <form method="POST" enctype="multipart/form-data" @submit.prevent="saveMovie" id="movieForm">
        
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" class="form-control" />
        </div>

        <div class="form-group mb-3">
            <label for="description" class="form-label">Movie Description</label>
            <textarea name="description" class="form-control" ></textarea>
        </div>

        <div class="form-group mb-3">
            <label for="poster" class="form-label">Movie Poster</label>
            <input type="file" name="poster" class="form-control"  />
        </div>
            
        <div class="form-group mb-3">
            <button type="submit" class="btn btn-primary" @change="onFileChange">Submit</button>
        </div>
    </form>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  name: "MovieForm",
  setup() {
    let csrf_token = ref("");
    function getCsrfToken() {
      fetch('http://127.0.0.1:8080//api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          csrf_token.value = data.csrf_token;
        })
    }
    onMounted(() => {
      getCsrfToken();
    });
    function saveMovie() {
      let movieForm = document.getElementById('movieForm');
      let form_data = new FormData(movieForm);
      console.log('CSRF Token:', csrf_token.value);  
      fetch("http://127.0.0.1:8080/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
          'X-CSRFToken': csrf_token.value
        }
      })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        console.log(data);
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    return {
      csrf_token,
      saveMovie,
    }
  }
}
</script>