<template>
  <div style="width: 100%; flex: 1 1 auto;">
    <page-header-wrapper style="padding-bottom: 5px;">
      <a-card :bordered="false">
        <div class="table-page-search-wrapper">
          <a-form layout="inline">
            <a-row :gutter="48">
              <a-col :md="6" :sm="24">
                <a-form-item label="Has ProductId">
                  <a-select v-model="hasProductId" placeholder="请选择" default-value="" @change="onHasProductIdChange">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option value="true">true</a-select-option>
                    <a-select-option value="false">false</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="6" :sm="24">
                <a-form-item label="Enabled">
                  <a-select v-model="isEnabled" placeholder="请选择" default-value="" @change="onEnableChange">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option value="true">true</a-select-option>
                    <a-select-option value="false">false</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="6" :sm="24">
                <a-form-item label="TaskStatus">
                  <a-select v-model="taskStatus" placeholder="请选择" default-value="" @change="filterData">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option value="Waiting">Waiting</a-select-option>
                    <a-select-option value="Prepare">Prepare</a-select-option>
                    <a-select-option value="Finish">Finish</a-select-option>
                    <a-select-option value="Trigered">Trigered</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="6" :sm="24">
                <a-form-item label="Status">
                  <a-select v-model="status" placeholder="请选择" default-value="" @change="filterData">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option value="New">New</a-select-option>
                    <a-select-option value="Deleted">Deleted</a-select-option>
                    <a-select-option value="Active">Active</a-select-option>
                    <a-select-option value="Changed">Changed</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </div>
      </a-card>
    </page-header-wrapper>
    <button @click="enableSelectedRows()">Enable Selected Rows</button>
    <button @click="disableSelectedRows()">Disable Selected Rows</button>
    <button @click="runSelectedRows()">Run Selected Rows</button>
    <ag-grid-vue
      ref="grid"
      style="width: 99%; height: 500px;"
      class="ag-theme-alpine"
      :columnDefs="columnDefs"
      :rowData="rowData"
      :defaultColDef="defaultColDef"
      rowSelection="multiple"
      @grid-ready="onGridReady">
    </ag-grid-vue>
    <div class="ag-status-name-value" >
      <span>Row Count &nbsp;:</span>
      <span>{{ count }}</span>
    </div>
    <udpate-form
      ref="UpdateCategoryAndMenuIdForm"
      :visible="visible"
      :loading="confirmLoading"
      :model="mdl"
      @cancel="handleCancel"
      @ok="handleOk"
    />
  </div>
</template>

<script>
    import { AgGridVue } from 'ag-grid-vue'
    import { getProductTasksList, enableProductTasksList, runProductTasks } from '@/api/scrapytask'
    import UpdateCategoryAndMenuIdForm from './modules/UpdateCategoryAndMenuIdForm'
    import moment from 'moment'

    export default {
        name: 'ProductTask',
        data () {
            return {
                // Filter params
                hasProductId: '',
                isEnabled: '',
                taskStatus: '',
                status: '',
                // 高级搜索 展开/关闭
                advanced: false,
                // 查询参数
                queryParam: {},
                // UpdateCategoryAndMenuIdForm model
                visible: false,
                confirmLoading: false,
                mdl: null,
                columnDefs: null,
                rowData: null,
                rowDataCache: null,
                gridApi: null,
                columnApi: null,
                defaultColDef: null,
                autoGroupColumnDef: null,
                count: 0,
                selectedRowKeys: [],
                selectedRows: []
            }
        },
        components: {
            AgGridVue,
            'udpate-form': UpdateCategoryAndMenuIdForm
        },
        filters: {
          productIdFilter (type) {
            return null
          }
        },
        methods: {
            filterData () {
              let tempData = this.rowDataCache
              if (this.hasProductId === 'true') {
                tempData = tempData.filter(d => d.productId !== null)
              }
              if (this.hasProductId === 'false') {
                tempData = tempData.filter(d => d.productId === null)
              }
              if (this.isEnabled === 'true') {
                tempData = tempData.filter(d => d.enabled)
              }
              if (this.isEnabled === 'false') {
                tempData = tempData.filter(d => d.enabled === false)
              }
              if (this.taskStatus !== '') {
                tempData = tempData.filter(d => d.taskStatus === this.taskStatus)
              }
              if (this.status !== '') {
                tempData = tempData.filter(d => d.status === this.status)
              }
              this.rowData = tempData
              this.count = tempData.length
            },
            onGridReady (params) {
                this.gridApi = params.api
                this.columnApi = params.columnApi
            },
            getSelectedTaskIds () {
              const selectedNodes = this.gridApi.getSelectedNodes()
              const selectedData = selectedNodes.map(node => node.data)
              const ids = selectedData.map(d => d.id)
              return ids
            },
            enableSelectedRows () {
              const ids = this.getSelectedTaskIds()
              if (ids.length > 0) {
                const param = { TaskIds: ids, Enable: true }
                this.confirmLoading = true
                enableProductTasksList(param)
                      .then(res => {
                        this.confirmLoading = false
                        this.reloadData()
                        this.$message.info('enable 成功')
                      })
              } else {
                this.$message.warning('You need to select the rows to enable')
              }
            },
            disableSelectedRows () {
              const ids = this.getSelectedTaskIds()
              if (ids.length > 0) {
                const param = { TaskIds: ids, Enable: false }
                this.confirmLoading = true
                enableProductTasksList(param)
                      .then(res => {
                        this.confirmLoading = false
                        this.reloadData()
                        this.$message.info('disable 成功')
                      })
              } else {
                this.$message.warning('You need to select the rows to disable')
              }
            },
            runSelectedRows () {
              const ids = this.getSelectedTaskIds()
              if (ids.length > 0) {
                const params = { 'TaskIds': ids.toString() }
                this.confirmLoading = true
                runProductTasks(params)
                .then(res => {
                  this.confirmLoading = false
                      this.reloadData()
                      this.$message.info('run 成功')
                })
              } else {
                this.$message.warning('You need to select the rows to run')
              }
            },
            reloadData () {
              this.confirmLoading = true
              getProductTasksList()
              .then(res => {
                this.rowDataCache = res
                this.filterData()
                this.confirmLoading = false
              })
            },
            handleCancel () {
              this.visible = false
              const form = this.$refs.UpdateCategoryAndMenuIdForm.form
              form.resetFields() // 清理表单数据（可不做）
            },
            handleOk () {
              const form = this.$refs.UpdateCategoryAndMenuIdForm.form
              this.confirmLoading = true
              form.validateFields((errors, values) => {
                if (!errors) {
                  console.log('values', values)
                } else {
                  this.confirmLoading = false
                }
              })
            },
            toggleAdvanced () {
              this.advanced = !this.advanced
            },
            resetSearchForm () {
              this.queryParam = {
                date: moment(new Date())
              }
            },
            onHasProductIdChange () {
              console.log('hasProductId', this.hasProductId)
              this.filterData()
            },
            onNoProductIdChange () {
              console.log('noProductId', this.noProductId)
              console.log('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX', this.$refs)
              this.filterData()
            },
            onEnableChange () {
              console.log('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX', this.$refs)
              this.filterData()
            },
            onTaskStatusChange () {
              this.filterData()
            }
        },
        beforeMount () {
            this.columnDefs = [
                { headerName: 'id', field: 'id', checkboxSelection: true, width: '150', headerCheckboxSelection: true },
                { headerName: 'ProductId', field: 'productId', filter: true, width: '150' },
                { headerName: 'Enabled', field: 'enabled', filter: true },
                { headerName: 'Task Status', field: 'taskStatus', filter: true },
                { headerName: 'Status', field: 'status', filter: true },
                { headerName: 'project', field: 'projectName', width: '100', filter: true },
                { headerName: 'TreeId', field: 'categoryTreeId', filter: true, width: '300' },
                { headerName: 'Url', field: 'productUrl', filter: true, width: '300' },
                { headerName: 'Price', field: 'price', filter: true, width: '300' },
                { headerName: 'Seconds', field: 'seconds', filter: true, width: '300' },
                { headerName: 'Create', field: 'createDateTime' },
                { headerName: 'Update', field: 'updateDateTime' }
            ]
            this.defaultColDef = { resizable: true }
            this.autoGroupColumnDef = {
                headerName: 'Model',
                field: 'model',
                cellRenderer: 'agGroupCellRenderer',
                cellRendererParams: {
                    checkbox: true
                }
            }
            console.log('here')
            this.reloadData()
        }
    }
</script>
