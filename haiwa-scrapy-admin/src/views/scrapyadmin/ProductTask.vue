<template>
  <div style="width: 100%; flex: 1 1 auto;">
    <button @click="enableSelectedRows()">Enable Selected Rows</button>
    <button @click="disableSelectedRows()">Disable Selected Rows</button>
    <button @click="runSelectedRows()">Run Selected Rows</button>
    <ag-grid-vue
      style="width: 90%; height: 800px;"
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

    export default {
        name: 'ProductTask',
        data () {
            return {
                // UpdateCategoryAndMenuIdForm model
                visible: false,
                confirmLoading: false,
                mdl: null,
                columnDefs: null,
                rowData: null,
                gridApi: null,
                columnApi: null,
                defaultColDef: null,
                autoGroupColumnDef: null,
                count: 0
            }
        },
        components: {
            AgGridVue,
            'udpate-form': UpdateCategoryAndMenuIdForm
        },
        methods: {
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
              getProductTasksList()
              .then(res => {
                this.rowData = res
                this.count = res.length
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
            }
        },
        beforeMount () {
            this.columnDefs = [
                { headerName: 'id', field: 'id', checkboxSelection: true, width: '150', headerCheckboxSelection: true },
                { headerName: 'ProductId', field: 'productId', filter: true, width: '150' },
                { headerName: 'Enabled', field: 'enabled', filter: true },
                { headerName: 'Task Status', field: 'taskStatus', filter: true },
                { headerName: 'project', field: 'projectName', width: '100', filter: true },
                { headerName: 'TreeId', field: 'categoryTreeId', filter: true, width: '300' },
                { headerName: 'Url', field: 'productUrl', filter: true, width: '300' },
                { headerName: 'Price', field: 'price', filter: true, width: '300' },
                { headerName: 'Seconds', field: 'seconds', filter: true, width: '300' },
                { headerName: 'Create', field: 'createDateTime' },
                { headerName: 'Update', field: 'updateDateTime' },
                { headerName: 'Status', field: 'status', filter: true }
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
