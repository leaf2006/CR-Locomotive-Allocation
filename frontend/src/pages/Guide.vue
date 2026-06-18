<template>
  <n-card title="使用指南">
    <n-space vertical :size="20">
      <n-alert type="info">
        本系统用于查询中国铁路现役机车与动车组信息。
      </n-alert>

      <n-h3>基本查询</n-h3>
      <n-p>在查询页面，您可以通过以下条件进行搜索：</n-p>
      <n-ul>
        <n-li><strong>车型</strong>：从下拉列表中选择车型（如 HXD1D、CRH2A 等）</n-li>
        <n-li><strong>车号</strong>：输入车号进行模糊搜索（如输入 0001 可匹配所有以 0001 结尾的编号）</n-li>
        <n-li><strong>生产厂家</strong>：从下拉列表中选择生产厂家</n-li>
        <n-li><strong>配属</strong>：从下拉列表中选择配属单位</n-li>
      </n-ul>

      <n-h3>组合查询</n-h3>
      <n-p>您可以同时设置多个查询条件，系统会返回同时满足所有条件的结果。</n-p>

      <n-h3>快速筛选</n-h3>
      <n-p>在结果列表中：</n-p>
      <n-ul>
        <n-li>点击<strong>车型</strong>列 → 快速筛选该车型的所有车辆</n-li>
        <n-li>点击<strong>配属</strong>列 → 快速筛选该配属单位的所有车辆</n-li>
      </n-ul>

      <n-h3>查看详情</n-h3>
      <n-p>点击每行左侧的展开按钮（▶），可以查看该车辆的详细信息，包括备注、拍摄者、拍摄日期和照片。</n-p>

      <n-h3>清除查询</n-h3>
      <n-p>每个查询框右侧都有清除按钮（×），最右侧有"清除全部"按钮可重置所有条件。</n-p>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { NCard, NSpace, NAlert, NH3, NP, NUl, NLi } from 'naive-ui'
</script>
