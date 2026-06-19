import { computed, ref, watch } from 'vue'
import type { TrainItem, QueryState } from '@/types'

export function useFilter(
  rawData: { value: TrainItem[] },
  query: QueryState
) {
  const debouncedNumber = ref(query.number)
  let debounceTimer: ReturnType<typeof setTimeout> | null = null

  watch(() => query.number, (val) => {
    if (debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
      debouncedNumber.value = val
    }, 200)
  })

  const filteredData = computed(() => {
    return rawData.value.filter((item) => {
      if (query.model && item.model !== query.model) return false
      if (debouncedNumber.value && !item.number.includes(debouncedNumber.value)) return false
      if (query.manufacturer && item.manufacturer !== query.manufacturer) return false
      if (query.allocation && item.allocation !== query.allocation) return false
      return true
    })
  })

  return { filteredData }
}
