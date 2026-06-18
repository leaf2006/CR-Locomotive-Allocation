<template>
  <n-card title="关于">
    <n-space vertical :size="20">
      <n-h3>关于作者</n-h3>
      <div style="display: flex; align-items: center; gap: 20px;">
        <img :src="logoUrl" alt="Logo" width="120" height="120" style="border-radius: 8px; object-fit: cover; flex-shrink: 0;" />
        <div style="line-height: 1.8;">
          <strong>Leaf developer</strong>（leaf2006）
          <br />
          本职菜鸟火车迷，兼职菜鸟计算机爱好者
          <br />
          <n-a href="https://github.com/leaf2006" target="_blank">Github: leaf2006</n-a>
          &nbsp;
          <n-a href="https://space.bilibili.com/511840995?spm_id_from=333.1007.0.0" target="_blank">Bilibili: leafdeveloper</n-a>
        </div>
      </div>

      <n-h3>关于项目</n-h3>
      <n-h4>简介</n-h4>
      <n-p>
        Github 项目地址：<n-a href="https://github.com/leaf2006/CR-Locomotive-Allocation" target="_blank">https://github.com/leaf2006/CR-Locomotive-Allocation</n-a>
      </n-p>
      <n-p>
        轨上名录（CR-Locomotive-Allocation）是一个用于查询中国铁路现役机车与动车组信息的网页。从数据获取到前端呈现，完全开源，采用 AGPL-3.0 开源协议，欢迎您前往项目 repo 点点 star⭐，也欢迎您
        <n-a href="https://github.com/leaf2006/CR-Locomotive-Allocation/issues" target="_blank">提交 issues</n-a>
        和
        <n-a href="https://github.com/leaf2006/CR-Locomotive-Allocation/pulls" target="_blank">PR</n-a>
      </n-p>

      <n-h4>为什么开发这个项目？</n-h4>
      <n-p>首先，是因为我闲的没事干，想搞点长期一点的事情做做。</n-p>
      <n-p>
        其次，是因为本人是下关站的忠实用户，多次在下关站上投稿照片，但是下关站的网站架构较老，其网站内部也没有关于路局、机务段配属的分类，加上经常间歇性地无法访问，因此就像当年因为 A 站服务器不稳定，才有了 Mikufans（B 站）一样，编写了这个网站。
      </n-p>
      <n-p>
        因为有了下关站与 emu.passearch.info，我得以踩在这两位前人的肩膀上看世界。本网站使用了较新的 Native UI，界面美观简洁，支持亮色/暗色模式，并且针对车型、配属、生产厂家都有对应的分类。在这里对两位前辈表示敬意。
      </n-p>

      <n-h4>技术栈</n-h4>
      <n-p>前端：</n-p>
      <n-ul>
        <n-li>Vue 3（Composition API）</n-li>
        <n-li>Vite</n-li>
        <n-li>TypeScript</n-li>
        <n-li>Naive UI</n-li>
        <n-li>Vue Router</n-li>
        <n-li>一个叫 Claude Code 的天才程序员</n-li>
      </n-ul>
      <n-p>数据获取：</n-p>
      <n-ul>
        <n-li>Python</n-li>
        <n-li>Github Action</n-li>
      </n-ul>

      <n-h4>数据源</n-h4>
      <n-ul>
        <n-li>下关站：<n-a href="http://www.xiaguanzhan.com/" target="_blank">www.xiaguanzhan.com</n-a></n-li>
        <n-li>emu.passearch.info：<n-a href="https://emu.passearch.info/" target="_blank">emu.passearch.info</n-a></n-li>
      </n-ul>
      <n-p>其中，普速列车机车车辆的数据普遍来自于前者，动车组的数据普遍来自于后者。</n-p>

      <n-h4>声明</n-h4>
      <n-p>
        本项目所有的数据来源于第三方渠道，所有引用的机车/动车组图片全部引用于下关站，本网站引用这些图片仅供参考、学习交流使用，照片的版权归拍摄作者所有，本网站不会做任何事情。也请所有使用该网站的用户保护版权，禁止商业使用，禁止用于短视频发布。
      </n-p>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { NCard, NSpace, NH3, NH4, NP, NUl, NLi, NA } from 'naive-ui'
import logoUrl from '@/assets/icons/my_logo.png'
</script>
