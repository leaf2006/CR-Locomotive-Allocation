// raw_result.json 中的小项原始结构
export interface RawItem {
  id: string
  allocation?: string
  manufacturer?: string
  train_series?: string
  photo_url?: string
  photo_author?: string
  photo_date?: string
  pro_id?: string
  note?: string
}

// 前端标准化后的结构
export interface TrainItem {
  id: string
  model: string
  number: string
  manufacturer: string | null
  allocation: string | null
  photoUrl: string | null
  photoAuthor: string | null
  photoDate: string | null
  note: string | null
}

// 查询条件
export interface QueryState {
  model: string
  number: string
  manufacturer: string
  allocation: string
}

// 原始数据类型（大项 -> 小项数组）
export type RawData = Record<string, RawItem[]>
