<template>
  <div class="navbar bg-neutral border-b border-base-content/5">
    <div class="container mx-auto">
      <div class="flex-1 flex justify-center">
        <ul class="menu menu-horizontal px-1">
          <li><router-link to="/" class="btn btn-neutral text-white text-xl">Dashboard</router-link></li>
          <li><router-link to="/paper-rating" class="btn btn-neutral text-white text-xl">Paper</router-link></li>
          <li><router-link to="/changelog" class="btn btn-neutral text-white text-xl">Changelog</router-link></li>
          <li><router-link to="/about" class="btn btn-neutral text-white text-xl">About</router-link></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
}
</style>