<template>
  <page-header-wrapper>
    <a-card :bordered="false">
      <div class="table-operator">
        <a-button type="primary" icon="plus" @click="handleAdd">Create</a-button>
      </div>

      <s-table
        ref="table"
        size="default"
        rowKey="key"
        :columns="columns"
        :data="loadData"
        :alert="true"
        :rowSelection="rowSelection"
        showPagination="auto"
      >
        <span slot="serial" slot-scope="text, record, index">
          {{ index + 1 }}
        </span>
        <span slot="status" slot-scope="text">
          <a-badge :status="text | statusTypeFilter" :text="text | statusFilter" />
        </span>
        <span slot="description" slot-scope="text">
          <ellipsis :length="4" tooltip>{{ text }}</ellipsis>
        </span>

        <span slot="action" slot-scope="text, record">
          <template>
            <a @click="handleRun(record)">Run</a>
            <a-divider type="vertical" />
            <a @click="handleDel(record)">Delete</a>
          </template>
        </span>
      </s-table>

      <create-form
        ref="createModal"
        :visible="visible"
        :loading="confirmLoading"
        :model="mdl"
        @cancel="handleCancel"
        @ok="handleOk"
      />
      <step-by-step-modal ref="modal" @ok="handleOk"/>
    </a-card>
  </page-header-wrapper>
</template>

<script>
import moment from 'moment'
import { STable, Ellipsis } from '@/components'
import { getRoleList } from '@/api/manage'
import { getSpiderRootTaskList, saveSpiderRootTask, runSpiderRootTask, deleteSpiderRootTask } from '@/api/scrapytask'

import StepByStepModal from './modules/StepByStepModal'
import CreateForm from './modules/CreateProjectForm'

const columns = [
  {
    title: '#',
    dataIndex: 'id'
  },
    {
    title: 'ProjectName',
    dataIndex: 'projectName',
    scopedSlots: { customRender: 'projectName' }
  },
   {
    title: 'CreateDateTime',
    dataIndex: 'createDateTime',
    sorter: true
  },
   {
    title: 'UpdateDateTime',
    dataIndex: 'updateDateTime',
    sorter: true
  },
  {
    title: 'TaskStatus',
    dataIndex: 'taskStatus',
    scopedSlots: { customRender: 'taskStatus' }
  },
  {
    title: '操作',
    dataIndex: 'action',
    width: '150px',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'RootTask',
  components: {
    STable,
    Ellipsis,
    CreateForm,
    StepByStepModal
  },
  data () {
    this.columns = columns
    return {
      // create model
      visible: false,
      confirmLoading: false,
      mdl: null,
      // 高级搜索 展开/关闭
      advanced: false,
      // 查询参数
      queryParam: {},
      // 加载数据方法 必须为 Promise 对象
      loadData: parameter => {
        const requestParameters = Object.assign({}, parameter, this.queryParam)
        console.log('loadData request parameters:', requestParameters)
        return getSpiderRootTaskList(requestParameters)
          .then(res => {
            return res
          })
      },
      selectedRowKeys: [],
      selectedRows: []
    }
  },
  filters: {
    statusFilter (type) {
    //   return statusMap[type].text
    },
    statusTypeFilter (type) {
    //   return statusMap[type].status
    }
  },
  created () {
    getRoleList({ t: new Date() })
  },
  computed: {
    rowSelection () {
      return {
        selectedRowKeys: this.selectedRowKeys,
        onChange: this.onSelectChange
      }
    }
  },
  methods: {
    handleAdd () {
      this.mdl = null
      this.visible = true
    },
    handleEdit (record) {
      this.visible = true
      this.mdl = { ...record }
    },
    handleRun (record) {
      var param = { ...record }
      console.log('line 209 param', param)
      runSpiderRootTask(param)
            .then(res => {
              this.confirmLoading = false
              this.$refs.table.refresh()
              this.$message.info('run 成功')
            })
    },
    handleDel (record) {
      var param = { ...record }
      console.log('line 209 param', param)
      deleteSpiderRootTask(param)
            .then(res => {
              this.confirmLoading = false
              this.$refs.table.refresh()
              this.$message.info('delete 成功')
            })
    },
    handleOk () {
      const form = this.$refs.createModal.form
      this.confirmLoading = true
      form.validateFields((errors, values) => {
        if (!errors) {
          console.log('values', values)
          if (values.id > 0) {
          } else {
            const requestParameters = Object.assign({}, values)
            console.log('line 252 requestParameters', requestParameters)
            saveSpiderRootTask(requestParameters)
            .then(res => {
              this.visible = false
              this.confirmLoading = false
              // 重置表单数据
              form.resetFields()
              // 刷新表格
              this.$refs.table.refresh()
              this.$message.info('新增成功')
            })
          }
        } else {
          this.confirmLoading = false
        }
      })
    },
    handleCancel () {
      this.visible = false
      const form = this.$refs.createModal.form
      form.resetFields() // 清理表单数据（可不做）
    },
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    resetSearchForm () {
      this.queryParam = {
        date: moment(new Date())
      }
    }
  }
}
</script>
