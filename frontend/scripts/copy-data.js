import { mkdirSync, copyFileSync, existsSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const src = resolve(__dirname, '../../data/raw_result.json')
const destDir = resolve(__dirname, '../public/data')
const dest = resolve(destDir, 'raw_result.json')

if (!existsSync(destDir)) {
  mkdirSync(destDir, { recursive: true })
}

copyFileSync(src, dest)
console.log('✅ data/raw_result.json → frontend/public/data/raw_result.json')
