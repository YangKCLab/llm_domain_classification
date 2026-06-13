<script setup>
import { ref, onMounted, computed } from 'vue'
import { useCompanyLogos } from '../composables/useCompanyLogos'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const { companyLogos, formatCompany, getCompanyLogo } = useCompanyLogos()

const totalNumberOfDomains = 5653
const results = ref([])
const selectedCompanies = ref([])
const showReasoningOnly = ref(false)

// Get unique companies from results
const uniqueCompanies = computed(() => {
  const companies = new Set(results.value.map(result => result.company))
  return Array.from(companies).sort()
})

const correlationResults = computed(() => {
  return results.value
    .filter(result => {
      const companyMatch = selectedCompanies.value.length === 0 || selectedCompanies.value.includes(result.company)
      const reasoningMatch = !showReasoningOnly.value || result.reasoning_type === 'reasoning'
      return companyMatch && reasoningMatch
    })
    .map(result => ({
      model_name: result.model_name,
      n: result.n,
      rho: result.rho,
      rho_p: result.rho_p,
      company: result.company,
      date: result.date,
      reasoning_type: result.reasoning_type
    }))
    .sort((a, b) => b.rho - a.rho) // Sort by rho in descending order
})

const biasResults = computed(() => {
  let biasResults_internal = results.value
    .filter(result => {
      const companyMatch = selectedCompanies.value.length === 0 || selectedCompanies.value.includes(result.company)
      const reasoningMatch = !showReasoningOnly.value || result.reasoning_type === 'reasoning'
      return companyMatch && reasoningMatch
    })
    .map(result => ({
      model_name: result.model_name,
      left_n: result.left_n,
      right_n: result.right_n,
      t: result.t,
      t_p: result.t_p,
      company: result.company,
      date: result.date,
      reasoning_type: result.reasoning_type
    }))
    .sort((a, b) => a.t - b.t) // Sort by t in ascending order
  biasResults_internal.forEach(result => {
    if (result.t < 0 && result.t_p < 0.05) {
      result.bias = 'left'
    } else if (result.t > 0 && result.t_p < 0.05) {
      result.bias = 'right'
    } else {
      result.bias = 'neutral'
    }
  })
  return biasResults_internal
})

onMounted(async () => {
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}data/results.json`)
    const text = await response.text()
    // Split by newlines and parse each line as JSON
    results.value = text.trim().split('\n').map(line => JSON.parse(line))
  } catch (error) {
    console.error('Error loading results:', error)
  }
})

// Format number to 3 decimal places
const formatNumber = (num) => Number(num).toFixed(2)
const formatPercentage = (num) => (num / totalNumberOfDomains * 100).toFixed(1)
const formatBias = (bias) => {
  if (bias === 'left') return 'L+'
  if (bias === 'right') return 'R+'
  return 'N'
}

// Convert p-value to significance stars
const pValueToStars = (pValue) => {
  if (pValue < 0.001) return '***'
  if (pValue < 0.01) return '**'
  if (pValue < 0.05) return '*'
  return 'NS' // Not significant
}

// Format p-value with stars
const formatPValue = (pValue) => {
  const stars = pValueToStars(pValue)
  return stars
}

// Check if date is within a month
const isWithinMonth = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays <= 30
}
</script>

<template>
  <div class="space-y-8 mb-8">
    <!-- Correlation Results Table -->
    <h1 class="text-3xl text-center font-bold my-6">Accuracy and political bias of news source credibility ratings by large language models</h1>

    <!-- Filters -->
    <div class="flex flex-col gap-4 justify-center items-center mb-6">
      <div class="flex flex-wrap gap-4 items-center">
        <div class="flex flex-wrap gap-2">
          <label v-for="company in uniqueCompanies" :key="company" class="label cursor-pointer gap-2">
            <input
              type="checkbox"
              class="checkbox checkbox-sm"
              :value="company"
              v-model="selectedCompanies"
            />
            <span class="label-text flex items-center gap-1">
              <img v-if="companyLogos[company]" :src="companyLogos[company]" :alt="company" class="h-4 inline-block" />
              {{ company }}
            </span>
          </label>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <label class="label cursor-pointer gap-2">
          <input
            type="checkbox"
            class="checkbox checkbox-sm"
            v-model="showReasoningOnly"
          />
          <span class="label-text flex items-center gap-1">
            <font-awesome-icon icon="brain" class="text-accent" />
            Reasoning models only
          </span>
        </label>
      </div>
    </div>

    <!-- Accuracy Results Table -->
    <h2 class="text-xl text-center font-bold mb-4">Accuracy (measured by correlation with human expert ratings)</h2>
    <div class="rounded-box border border-base-content/5 bg-base-100">
      <table class="table table-zebra w-full">
        <thead>
          <tr class="bg-base-200">
            <th>
              Model
              <div class="tooltip tooltip-right" data-tip="Large Language Model variant used for testing">
                <span class="text-xs ml-1 opacity-50 cursor-help">?</span>
              </div>
            </th>
            <th class="text-right">
              N (%)
              <div class="tooltip tooltip-right" data-tip="Number of domains rated by the model (percentage in all tested domains)">
                <span class="text-xs ml-1 opacity-50 cursor-help">?</span>
              </div>
            </th>
            <th class="text-right">
              Spearman's ρ
              <div class="tooltip tooltip-left" data-tip="Spearman's rank correlation coefficient between model ratings and human expert ratings. The stars indicate the significance level of the correlation coefficient: *** p < 0.001, ** p < 0.01, * p < 0.05, NS p >= 0.05">
                <span class="text-xs ml-1 opacity-50 cursor-help">?</span>
              </div>
            </th>
            <th class="text-right">
              Company
              <div class="tooltip tooltip-right" data-tip="Company that developed the model">
                <span class="text-xs ml-1 opacity-50 cursor-help">?</span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in correlationResults" :key="result.model_name" class="hover">
            <td class="font-mono text-sm">
              <img v-if="getCompanyLogo(result.company)" :src="getCompanyLogo(result.company)" :alt="result.company" class="h-4 inline-block mr-2" />
              {{ result.model_name }}
              <font-awesome-icon v-if="result.reasoning_type === 'reasoning'" icon="brain" class="ml-1 text-accent" />
              <span v-if="isWithinMonth(result.date)" class="badge badge-outline badge-accent badge-sm ml-1">New</span>
            </td>
            <td class="text-right font-mono">{{ result.n }}({{ formatPercentage(result.n) }}%)</td>
            <td class="text-right font-mono">
              {{ formatNumber(result.rho) }}
              <span class="badge badge-info-content badge-outline badge-sm ml-1 opacity-40 cursor-help">{{ formatPValue(result.rho_p) }} </span>
            </td>
            <td class="text-right">{{ result.company }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Bias Results Table -->
    <h2 class="text-xl text-center font-bold mb-4">Political bias measurement</h2>
    <div class="rounded-box border border-base-content/5 bg-base-100">
      <table class="table table-zebra w-full">
        <thead>
          <tr class="bg-base-200">
            <th>
              Model
              <div class="tooltip tooltip-right" data-tip="Large Language Model variant used for testing">
                <span class="text-xs ml-1 opacity-50 cursor-help">?</span>
              </div>
            </th>
            <th class="text-right">
              No. Left | Right
              <div class="tooltip tooltip-right" data-tip="Number of domains classified as left-leaning vs right-leaning and rated by the model">
                <span class="text-xs ml-1 opacity-50 cursor-help">?</span>
              </div>
            </th>
            <th class="text-right">
              t-statistic
              <div class="tooltip tooltip-left" data-tip="T-statistic measuring the bias of the model's rating. Negative t-values indicate left-leaning bias (L+), positive t-values indicate right-leaning bias (R+). See methods below for more details. The stars indicate the significance level of the t-statistic: *** p < 0.001, ** p < 0.01, * p < 0.05, NS p >= 0.05">
                <span class="text-xs ml-1 opacity-50 cursor-help">?</span>
              </div>
            </th>
            <th class="text-right">
              Company
              <div class="tooltip tooltip-right" data-tip="Company that developed the model">
                <span class="text-xs ml-1 opacity-50 cursor-help">?</span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in biasResults" :key="result.model_name" class="hover">
            <td class="font-mono text-sm">
              <img v-if="getCompanyLogo(result.company)" :src="getCompanyLogo(result.company)" :alt="result.company" class="h-4 inline-block mr-2" />
              {{ result.model_name }}
              <font-awesome-icon v-if="result.reasoning_type === 'reasoning'" icon="brain" class="ml-1 text-accent" />
              <span v-if="isWithinMonth(result.date)" class="badge badge-outline badge-accent badge-sm ml-1">New</span>
            </td>
            <td class="text-right font-mono">
                <div class="flex justify-end items-center gap-2">
                    <span class="text-info-content">{{ result.left_n }}</span>
                    <span class="opacity-50">|</span>
                    <span class="text-error-content">{{ result.right_n }}</span>
                </div>
            </td>
            <td class="text-right font-mono" :class="result.bias === 'left' ? 'text-info-content' : result.bias === 'right' ? 'text-error-content' : ''">
              {{ formatNumber(result.t) }}
              <span class="badge badge-info-content badge-outline badge-sm ml-1 opacity-40 cursor-help">{{ formatPValue(result.t_p) }} </span>
              <span class="badge badge-info-content badge-outline badge-sm ml-1 opacity-40 cursor-help">{{ formatBias(result.bias) }}</span>
            </td>
            <td class="text-right">{{ result.company }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- methods -->
    <h2 class="text-xl text-center font-bold mb-4">Methods</h2>
    <div class="prose prose-slate max-w-none">
      <p>
        Large Language Models (LLMs) are increasingly used as information curators in our daily lives in search engines, chatbots, and recommendation systems.
        But can they accurately evaluate news sources?
      </p>
      <p>
        To answer this question, we use a pre-defined list of 5,653 news domains with credibility ratings <a href="https://academic.oup.com/pnasnexus/article/2/9/pgad286/7258994" target="_blank">produced by human experts</a> as our ground truth.
        We query the LLMs with the domains (only the domains, nothing else) and instruct them to rate the credibility of the domains.
        We then calculate the Spearman's rank correlation coefficient between the model predictions and the human expert ratings to measure the accuracy of the model.
      </p>
      <p>
        The domains are also <a href="https://github.com/LazerLab/DomainDemo" target="_blank">classified as left- or right-leaning</a> to measure the political bias of the LLMs.
        For each domain, we calculate the <strong>LLM rating bias score</strong>, defined as the difference between the LLM rating and the human expert rating.
        This metric accounts for the fact that left-leaning sources in our dataset tend to have higher human expert ratings.
        A positive/negative bias score means the LLM considers the source more/less credible than expected.
        We then compare the LLM rating bias scores for left- and right-leaning domains through t-tests between the two groups.
        The t-statistic indicates the bias of the LLM.
      </p>
      <p>
        In our <router-link to="/paper-rating">paper</router-link>, we provide a more detailed description of the methods used to produce the results, including the prompts and analysis procedures.
        Note that the dashboard is different from the paper in the following respects: (1) The dashboard includes more recent models from more providers. (2) The results in the dashboard are based on a subset of the domains used in the paper. Only 5,653 domains are used in the dashboard. (3) The dashboard leverages a more comprehensive <a href="https://github.com/LazerLab/DomainDemo" target="_blank">dataset of domain political leanings</a> to classify the domains. All 5,653 domains has political leaning scores. In the paper, only 2,683 domains have political leaning scores.
      </p>
      <p>
        If you are interested in the source code behind this dashboard, it's available <a href="https://github.com/YangKCLab/llm_domain_classification" target="_blank">here</a>.
      </p>
    </div>

    <!-- Citation -->
    <h2 class="text-xl text-center font-bold mb-4">Citation</h2>
    <div class="prose prose-slate max-w-none">
      <p>
        If you use this dashboard in your work, please cite this <router-link to="/paper-rating">paper</router-link>.
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Custom tooltip styling */
:deep(.tooltip) {
  --tooltip-color: #1f2937; /* Dark background */
  --tooltip-text-color: white; /* White text */
}

:deep(.tooltip::before) {
  background-color: var(--tooltip-color) !important;
  color: var(--tooltip-text-color) !important;
  padding: 0.5rem 0.75rem !important;
  font-size: 0.875rem !important;
  max-width: 20rem !important;
  border-radius: 0.375rem !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
}
</style>