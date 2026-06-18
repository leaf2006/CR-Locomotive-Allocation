<template>
  <n-card title="数据有误？">
    <n-space vertical :size="20">
      <n-p>
        由于本网站数据全部来源于第三方，所以出现错误的概率很大。常见的错误如配属信息过时，您可以通过<strong>以下方式反馈</strong>。
      </n-p>

      <n-alert type="warning">
        由于下关站是本网站重要的数据获取来源，如果数据有误，在我们核验过后，我们会直接下架本网站上关于该车号的，来自下关站的旧图。
      </n-alert>

      <n-h3>反馈方式</n-h3>
      <n-ul>
        <n-li>
          您可以通过
          <n-a href="https://github.com/leaf2006/CR-Locomotive-Allocation/issues" target="_blank">Github Issues</n-a>
          反馈数据的错误
        </n-li>
        <n-li>
          您也可以通过
          <n-a href="https://github.com/leaf2006/CR-Locomotive-Allocation/pulls" target="_blank">Pull Requests</n-a>
          直接申请修改 <n-text code>fix.json</n-text> 文件，该文件包含所有勘误信息
        </n-li>
      </n-ul>

      <n-h3>反馈要求</n-h3>
      <n-p>通过 Github Issues 反馈的用户，请您在提交 issue 的时候注明以下信息：</n-p>
      <n-ul>
        <n-li>车号 (id)</n-li>
        <n-li>正确的车辆配属 (allocation)</n-li>
        <n-li>正确的车辆生产厂家 (manufacturer)</n-li>
        <n-li>备注，可选填 (note)</n-li>
      </n-ul>

      <n-p>
        通过 Pull Requests 反馈的用户，请您根据以下标准修改 <n-text code>fix.json</n-text> 代码块：
      </n-p>
      <n-code :code="sampleJson" language="json" />

      <n-p style="margin-top: 8px; font-weight: bold;">
        感谢您的指正！
      </n-p>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { NCard, NSpace, NAlert, NH3, NP, NUl, NLi, NA, NText, NCode } from 'naive-ui'

const sampleJson = `{
  "allocation": "配属(上局沪段)",
  "id": "车号(DF4-XXXX)",
  "manufacturer": "生产厂家(中车资阳机车)",
  "note": "选填",
  "pro_id": "别填",
  "train_series": "车型(DF4)"
}`
</script>
