<template>
  <div class="container mx-auto p-4">
    <h1 class="title">Busca de Operadoras</h1>
    
    <div class="search-container">
      <input 
        v-model="searchQuery" 
        @keyup.enter="searchOperadoras"
        class="search-input"
        placeholder="Digite sua busca..."
      />
      <button 
        @click="searchOperadoras"
        class="search-button"
      >
        Buscar
      </button>
    </div>
    
    <div v-if="loading" class="loading">Carregando...</div>
    
    <div v-if="error" class="error">{{ error }}</div>
    
    <div v-if="results.length" class="results-container">
      <p class="results-count">Total de resultados: {{ totalResults }}</p>
      
      <div class="table-responsive">
        <table class="results-table">
          <thead>
            <tr>
              <th>Registro ANS</th>
              <th>Nome Fantasia</th>
              <th>CNPJ</th>
              <th>Modalidade</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in results" :key="item.Registro_ANS" class="table-row">
              <td>{{ item.Registro_ANS }}</td>
              <td>{{ item.Nome_Fantasia }}</td>
              <td>{{ item.CNPJ }}</td>
              <td>{{ item.Modalidade }}</td>
            </tr>
          </tbody>
        </table>
      </div>
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

<style scoped>
.container {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  max-width: 1280px;
  margin: 0 auto;
  line-height: 1.5;
  color: #213547;
  background-color: #ffffff;
}

.title {
  font-size: 1.75rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
}

.search-container {
  display: flex;
  margin-bottom: 1rem;
  width: 100%;
}

.search-input {
  flex-grow: 1;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem 0 0 0.25rem;
  font-size: 1rem;
}

.search-button {
  background-color: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0 0.25rem 0.25rem 0;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.search-button:hover {
  background-color: #2563eb;
}

.loading {
  text-align: center;
  padding: 1rem;
  font-weight: 500;
  color: #6b7280;
}

.error {
  color: #ef4444;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 0.25rem;
  background-color: #fee2e2;
  text-align: center;
}

.results-container {
  margin-top: 1rem;
}

.results-count {
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.table-responsive {
  overflow-x: auto;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-radius: 0.375rem;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
}

.results-table th {
  background-color: #f3f4f6;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #d1d5db;
}

.results-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
  white-space: nowrap;
}

.table-row:hover {
  background-color: #f9fafb;
}

@media (max-width: 768px) {
  .title {
    font-size: 1.5rem;
  }
  
  .search-input, .search-button {
    padding: 0.5rem;
  }
  
  .search-button {
    white-space: nowrap;
  }
  
  .results-table th, .results-table td {
    padding: 0.5rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 640px) {
  .search-container {
    flex-direction: column;
  }
  
  .search-input {
    border-radius: 0.25rem 0.25rem 0 0;
  }
  
  .search-button {
    border-radius: 0 0 0.25rem 0.25rem;
    width: 100%;
  }
}
</style>