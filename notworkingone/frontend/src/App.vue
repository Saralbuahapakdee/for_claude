<template>
  <div id="app">
    <div class="container">
      <h1 class="title">Weapon Detection Stream (via Flask Auth)</h1>

      <div v-if="!token" class="login-form">
        <input
          v-model="username"
          placeholder="Username"
          class="input-field"
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          class="input-field"
        />
        <button @click="login" class="login-btn">Login</button>
      </div>

      <div v-else class="stream-container">
        <h3 class="stream-title">Live AI Stream</h3>
        <img :src="videoUrl" class="video-stream" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"

const username = ref("admin")
const password = ref("admin123")
const token = ref("")
const videoUrl = ref("")

async function login() {
  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: username.value, password: password.value })
  })
  const data = await res.json()
  if (data.access_token) {
    token.value = data.access_token
    videoUrl.value = `/api/video?token=${token.value}`
  }
}
</script>

<style scoped>
/* Global Reset and Full Viewport */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  overflow: hidden; /* No scrollbars */
}

#app {
  height: 100vh; /* Full viewport height */
  width: 100vw;  /* Full viewport width */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden; /* No scrollbars */
}

.container {
  width: 100vw;            /* Full viewport width */
  height: 100vh;           /* Full viewport height */
  padding: 20px;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  text-align: center;
  overflow: hidden; /* No scrollbars */
}

.title {
  font-size: 2.5rem;
  color: #4a90e2;
  margin-bottom: 30px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.input-field {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  width: 300px;
  margin: 0 auto;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #4a90e2;
  outline: none;
}

.login-btn {
  padding: 12px 20px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 320px;
  margin: 0 auto;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.login-btn:hover {
  background-color: #357ab7;
}

.stream-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}

.stream-title {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: #333;
}

.video-stream {
  max-width: 100%;
  max-height: calc(100vh - 100px); /* Constrain to viewport minus title space */
  width: auto;
  height: auto;
  object-fit: contain; /* Maintain aspect ratio */
  border-radius: 8px;
  border: 1px solid #ddd;
}
</style>