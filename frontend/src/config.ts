/**
 * 全局配置
 *
 * 图片代理：原站 xiaguanzhan.com 不支持 HTTPS，GitHub Pages 强制 HTTPS
 * 导致 Mixed Content 被浏览器阻止。通过公共图片代理转发请求。
 *
 * 替换代理源时只需修改 IMAGE_PROXY_PREFIX 的值。
 */
export const IMAGE_PROXY_PREFIX = 'https://images.weserv.nl/?url='
