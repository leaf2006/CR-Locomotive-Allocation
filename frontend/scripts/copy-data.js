import { mkdirSync, copyFileSync, existsSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const destDir = resolve(__dirname, '../public/data')

if (!existsSync(destDir)) {
  mkdirSync(destDir, { recursive: true })
}

const files = [
  { src: '../../data/raw_result.json', name: 'raw_result.json' },
  { src: '../../data/version.txt', name: 'version.txt' },
]

for (const file of files) {
  const srcPath = resolve(__dirname, file.src)
  const destPath = resolve(destDir, file.name)
  if (existsSync(srcPath)) {
    copyFileSync(srcPath, destPath)
    console.log(`✅ data/${file.name} → frontend/public/data/${file.name}`)
  }
}
