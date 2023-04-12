<template>
    <div class="container">
      <h1>Movies</h1>
      <div class="movies-view">
        <div v-for="movie in movies" :key="movie.id" class="cards">
          <img :src="movie.poster" alt="Movie Poster" />
          <div class="text">
            <h2 class="title">{{ movie.title }}</h2>
            <p class="desc">{{ movie.description }}</p>
          </div>
          </div>
      </div>
    </div>
  </template>
  
  <style>
  .movies-view {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-row-gap: 20px;
    grid-column-gap: 70px;
  }
  .cards {
    background-color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items:normal;
    border-radius: 5px;
  }
  .cards img {
    max-width: 100%;
    height: 100%;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
  }
  .text{
    margin-right: 30px;
    padding: 10px;
  }
  </style>
  
  <script setup>
  import { ref, onMounted } from "vue";
  let movies = ref([]);
  const fetchMovies = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8080//api/v1/movies");
      const data = await response.json();
      movies.value = data.movies;
    } catch (error) {
      console.log(error);
    }
  };
  onMounted(() => {
    fetchMovies();
  });
  </script>