<template>
    <div>
      <h1>Add Movie</h1>
      <movie-form />
    </div>
  </template>
  
  <script>
  import MovieForm from "@/components/MovieForm.vue";
  
  export default {
    name: "AddMovieFormView",
    components: {
      MovieForm,
    },
  };
  </script>
  