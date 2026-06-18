import { reactive } from 'vue'
import type { QueryState } from '@/types'

const query = reactive<QueryState>({
  model: '',
  number: '',
  manufacturer: '',
  allocation: '',
})

export function useQuery() {
  function clearModel() { query.model = '' }
  function clearNumber() { query.number = '' }
  function clearManufacturer() { query.manufacturer = '' }
  function clearAllocation() { query.allocation = '' }

  function clearAll() {
    query.model = ''
    query.number = ''
    query.manufacturer = ''
    query.allocation = ''
  }

  function setModel(model: string) { query.model = model }
  function setAllocation(allocation: string) { query.allocation = allocation }

  return {
    query,
    clearModel,
    clearNumber,
    clearManufacturer,
    clearAllocation,
    clearAll,
    setModel,
    setAllocation,
  }
}
