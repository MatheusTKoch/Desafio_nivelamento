<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Busca de Operadoras</h1>
    
    <div class="flex mb-4">
      <input 
        v-model="searchQuery" 
        @keyup.enter="searchOperadoras"
        class="flex-grow p-2 border rounded-l"
        placeholder="Digite sua busca..."
      />
      <button 
        @click="searchOperadoras"
        class="bg-blue-500 text-white px-4 py-2 rounded-r"
      >
        Buscar
      </button>
    </div>
    
    <div v-if="loading" class="text-center">Carregando...</div>
    
    <div v-if="error" class="text-red-500">{{ error }}</div>
    
    <div v-if="results.length" class="mt-4">
      <p class="mb-2">Total de resultados: {{ totalResults }}</p>
      
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-gray-200">
            <th class="border p-2">Registro ANS</th>
            <th class="border p-2">Nome Fantasia</th>
            <th class="border p-2">CNPJ</th>
            <th class="border p-2">Modalidade</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.Registro_ANS" class="hover:bg-gray-100">
            <td class="border p-2">{{ item.Registro_ANS }}</td>
            <td class="border p-2">{{ item.Nome_Fantasia }}</td>
            <td class="border p-2">{{ item.CNPJ }}</td>
            <td class="border p-2">{{ item.Modalidade }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const results = ref([])
const totalResults = ref(0)
const loading = ref(false)
const error = ref(null)

// Pesquisa de operadoras
const searchOperadoras = async () => {
  results.value = []
  error.value = null
  loading.value = true
  
  try {
    const response = await axios.get('http://localhost:5000/search', {
      params: { q: searchQuery.value }
    })
    
    results.value = response.data.results
    totalResults.value = response.data.total_results
  } catch (err) {
    error.value = 'Erro ao buscar operadoras: ' + err.message
  } finally {
    loading.value = false
  }
}
</script>