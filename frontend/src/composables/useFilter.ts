import { computed } from 'vue'
import type { TrainItem, QueryState } from '@/types'

export function useFilter(
  rawData: { value: TrainItem[] },
  query: QueryState
) {
  const filteredData = computed(() => {
    return rawData.value.filter((item) => {
      if (query.model && item.model !== query.model) return false
      if (query.number && !item.number.includes(query.number)) return false
      if (query.manufacturer && item.manufacturer !== query.manufacturer) return false
      if (query.allocation && item.allocation !== query.allocation) return false
      return true
    })
  })

  return { filteredData }
}
