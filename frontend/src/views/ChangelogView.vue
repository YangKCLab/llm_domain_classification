<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import { useCompanyLogos } from '@/composables/useCompanyLogos'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const { getCompanyLogo } = useCompanyLogos()

const results = ref([])

onMounted(async () => {
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}data/results.json`)
    const text = await response.text()
    results.value = text.trim().split('\n').map(line => JSON.parse(line))
  } catch (error) {
    console.error('Error loading results:', error)
  }
})

// Format rho to 2 decimal places
const formatNumber = (num) => Number(num).toFixed(2)

// Check if date is within a month
const isWithinMonth = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays <= 30
}

// Group results by date, newest first; within each date sort by model_name
const groupedByDate = computed(() => {
  const grouped = results.value.reduce((acc, model) => {
    const date = model.date
    if (!acc[date]) acc[date] = []
    acc[date].push(model)
    return acc
  }, {})

  return Object.keys(grouped)
    .sort((a, b) => b.localeCompare(a)) // newest first
    .map(date => ({
      date,
      models: grouped[date].slice().sort((a, b) => a.model_name.localeCompare(b.model_name)),
    }))
})
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <NavBar />
    <div class="container mx-auto flex-grow px-4 py-8">
      <h1 class="text-3xl text-center font-bold mb-2">Changelog</h1>
      <p class="text-center text-base-content/60 mb-8">
        Models added over time — see the
        <router-link to="/" class="link link-neutral">Dashboard</router-link>
        for full stats and filters.
      </p>

      <div v-if="groupedByDate.length === 0" class="text-center text-base-content/40 py-16">
        Loading…
      </div>

      <div v-else class="space-y-8 max-w-2xl mx-auto">
        <div v-for="group in groupedByDate" :key="group.date">
          <!-- Date heading -->
          <div class="flex items-center gap-3 mb-3">
            <span class="text-lg font-semibold font-mono">{{ group.date }}</span>
            <span
              v-if="isWithinMonth(group.date)"
              class="badge badge-outline badge-accent badge-sm"
            >New</span>
            <div class="flex-1 border-t border-base-content/10"></div>
            <span class="text-base-content/40 text-sm">{{ group.models.length }} model{{ group.models.length !== 1 ? 's' : '' }}</span>
          </div>

          <!-- Model list -->
          <div class="rounded-box border border-base-content/5 bg-base-100 divide-y divide-base-content/5">
            <div
              v-for="model in group.models"
              :key="model.model_name"
              class="flex items-center gap-3 px-4 py-3 hover:bg-base-200/50 transition-colors"
            >
              <!-- Logo -->
              <img
                v-if="getCompanyLogo(model.company)"
                :src="getCompanyLogo(model.company)"
                :alt="model.company"
                class="h-4 flex-shrink-0"
              />
              <!-- Model name -->
              <span class="font-mono text-sm flex-1 min-w-0 truncate">
                {{ model.model_name }}
              </span>
              <!-- Reasoning icon -->
              <font-awesome-icon
                v-if="model.reasoning_type === 'reasoning'"
                icon="brain"
                class="text-accent flex-shrink-0"
                title="Reasoning model"
              />
              <!-- Company -->
              <span class="text-base-content/50 text-sm flex-shrink-0">{{ model.company }}</span>
              <!-- Rho -->
              <span class="font-mono text-sm flex-shrink-0">
                ρ = {{ formatNumber(model.rho) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>
