import { ref, onMounted } from 'vue'
import type { RawData, RawItem, TrainItem } from '@/types'

const rawData = ref<TrainItem[]>([])
const models = ref<string[]>([])
const manufacturers = ref<string[]>([])
const allocations = ref<string[]>([])
const loading = ref(true)

function normalizeField(value: string | undefined | null): string | null {
  if (value === undefined || value === null || value === '') return null
  return value
}

function extractNumber(id: string): string {
  const parts = id.split('-')
  return parts[parts.length - 1] || ''
}

function flattenData(data: RawData): TrainItem[] {
  const result: TrainItem[] = []
  for (const [model, items] of Object.entries(data)) {
    for (const item of items) {
      result.push({
        id: item.id,
        model,
        number: extractNumber(item.id),
        manufacturer: normalizeField(item.manufacturer),
        allocation: normalizeField(item.allocation),
        photoUrl: normalizeField(item.photo_url),
        photoAuthor: normalizeField(item.photo_author),
        photoDate: normalizeField(item.photo_date),
        note: normalizeField(item.note),
      })
    }
  }
  return result
}

export function useData() {
  onMounted(async () => {
    if (rawData.value.length > 0) {
      loading.value = false
      return
    }
    try {
      const response = await fetch('./data/raw_result.json')
      const data: RawData = await response.json()
      rawData.value = flattenData(data)
      models.value = Object.keys(data).sort()
      const mfgSet = new Set<string>()
      const allocSet = new Set<string>()
      for (const item of rawData.value) {
        if (item.manufacturer) mfgSet.add(item.manufacturer)
        if (item.allocation) allocSet.add(item.allocation)
      }
      manufacturers.value = [...mfgSet].sort()
      allocations.value = [...allocSet].sort()
    } catch (e) {
      console.error('Failed to load data:', e)
    } finally {
      loading.value = false
    }
  })

  return {
    rawData,
    models,
    manufacturers,
    allocations,
    loading,
  }
}
