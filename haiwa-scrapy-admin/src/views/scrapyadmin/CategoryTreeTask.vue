<template>
  <div style="width: 100%; flex: 1 1 auto;">
    <page-header-wrapper style="padding-bottom: 5px;">
      <a-card :bordered="false">
        <div class="table-page-search-wrapper">
          <a-form layout="inline">
            <a-row :gutter="48">
              <a-col :md="4" :sm="24">
                <a-form-item label="Enabled">
                  <a-select v-model="isEnabled" placeholder="请选择" default-value="" @change="filterData">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option value="true">true</a-select-option>
                    <a-select-option value="false">false</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="4" :sm="24">
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
              <a-col :md="4" :sm="24">
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
              <a-col :md="4" :sm="24">
                <a-form-item label="Project">
                  <a-select v-model="projectSelected" placeholder="请选择" default-value="" @change="loadLevelOption(1)">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option v-for="option in projectOptions" :key="option">
                      {{ option }}
                    </a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="6" :sm="24">
                <a-form-item label="L1">
                  <a-select v-model="level1Selected" placeholder="请选择" default-value="" @change="loadLevelOption(2)">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option v-for="option in level1Options" :key="option">
                      {{ option }}
                    </a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="6" :sm="24">
                <a-form-item label="L2">
                  <a-select v-model="level2Selected" placeholder="请选择" default-value="" @change="loadLevelOption(3)">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option v-for="option in level2Options" :key="option">
                      {{ option }}
                    </a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="6" :sm="24">
                <a-form-item label="L3">
                  <a-select v-model="level3Selected" placeholder="请选择" default-value="" @change="loadLevelOption(4)">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option v-for="option in level3Options" :key="option">
                      {{ option }}
                    </a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="6" :sm="24">
                <a-form-item label="L4">
                  <a-select v-model="level4Selected" placeholder="请选择" default-value="" @change="loadLevelOption(5)">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option v-for="option in level4Options" :key="option">
                      {{ option }}
                    </a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :md="6" :sm="24">
                <a-form-item label="L5">
                  <a-select v-model="level5Selected" placeholder="请选择" default-value="" @change="filterData">
                    <a-select-option value="">全部</a-select-option>
                    <a-select-option v-for="option in level5Options" :key="option">
                      {{ option }}
                    </a-select-option>
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
    <button @click="updateSelectedRows()">Update Category & MenufactoryId for Selected Rows</button>
    <button @click="runSelectedRows()">Run Selected Rows</button>
    <ag-grid-vue
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
    import { getSpiderCategoryTreeTasksList, enableSpiderCategoryTreeTasksList, updateCategoryAndManufactoryIdForTasks, disableSpiderCategoryTreeTasksList, runCategoryTreeTasks } from '@/api/scrapytask'
    import UpdateCategoryAndMenuIdForm from './modules/UpdateCategoryAndMenuIdForm'

    export default {
        name: 'CategoryTreeTask',
        data () {
            return {
                projectOptions: [],
                level1Options: [],
                level2Options: [],
                level3Options: [],
                level4Options: [],
                level5Options: [],
                projectSelected: '',
                level1Selected: '',
                level2Selected: '',
                level3Selected: '',
                level4Selected: '',
                level5Selected: '',
                // Filter params
                isEnabled: '',
                taskStatus: '',
                status: '',
                // UpdateCategoryAndMenuIdForm model
                visible: false,
                confirmLoading: false,
                mdl: null,
                columnDefs: null,
                rowDataCache: null,
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
            filterData () {
              let tempData = this.rowDataCache
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
              if (this.projectSelected !== '') {
                tempData = tempData.filter(d => d.projectName === this.projectSelected)
              }
              if (this.level1Selected !== '') {
                tempData = tempData.filter(d => d.categoryLevel1 === this.level1Selected)
              }
              if (this.level2Selected !== '') {
                tempData = tempData.filter(d => d.categoryLevel2 === this.level2Selected)
              }
              if (this.level3Selected !== '') {
                tempData = tempData.filter(d => d.categoryLevel3 === this.level3Selected)
              }
              if (this.level4Selected !== '') {
                tempData = tempData.filter(d => d.categoryLevel4 === this.level4Selected)
              }
              if (this.level5Selected !== '') {
                tempData = tempData.filter(d => d.categoryLevel5 === this.level5Selected)
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
              const param = { TaskIds: ids, Enable: true }
              enableSpiderCategoryTreeTasksList(param)
                    .then(res => {
                      this.confirmLoading = false
                      this.reloadData()
                      this.$message.info('enable 成功')
                    })
            },
            disableSelectedRows () {
              const ids = this.getSelectedTaskIds()
              const param = { TaskIds: ids, Enable: false }
              disableSpiderCategoryTreeTasksList(param)
                    .then(res => {
                      this.confirmLoading = false
                      this.reloadData()
                      this.$message.info('disable 成功')
                    })
            },
            updateSelectedRows () {
              const ids = this.getSelectedTaskIds()
              if (ids.length > 0) {
                this.mdl = { 'TaskIds': ids.toString() }
                this.visible = true
                console.log('line 8000', this.visible)
              } else {
                this.$message.warning('You need to select the rows to update')
              }
            },
            runSelectedRows () {
              const ids = this.getSelectedTaskIds()
              if (ids.length > 0) {
                const params = { 'TaskIds': ids.toString() }
                runCategoryTreeTasks(params)
                .then(res => {
                  this.confirmLoading = false
                      this.reloadData()
                      this.$message.info('disable 成功')
                })
              } else {
                this.$message.warning('You need to select the rows to run')
              }
            },
            reloadData () {
              getSpiderCategoryTreeTasksList()
              .then(res => {
                this.rowDataCache = res
                this.projectOptions = res.map(t => t.projectName).filter((value, index, self) => self.indexOf(value) === index)
                this.filterData()
              })
            },
            loadLevelOption (level) {
              switch (level) {
                case 1:
                  this.level1Selected = ''
                  this.level2Selected = ''
                  this.level3Selected = ''
                  this.level4Selected = ''
                  this.level5Selected = ''
                  this.level1Options = this.rowDataCache.filter(t => t.projectName === this.projectSelected).map(t => t.categoryLevel1).filter((value, index, self) => self.indexOf(value) === index)
                  this.level2Options = []
                  this.level3Options = []
                  this.level4Options = []
                  this.level5Options = []
                  break
                case 2:
                  this.level2Selected = ''
                  this.level3Selected = ''
                  this.level4Selected = ''
                  this.level5Selected = ''
                  this.level2Options = this.rowDataCache.filter(t => t.projectName === this.projectSelected && t.categoryLevel1 === this.level1Selected).map(t => t.categoryLevel2).filter((value, index, self) => self.indexOf(value) === index)
                  this.level3Options = []
                  this.level4Options = []
                  this.level5Options = []
                  break
                case 3:
                  this.level3Selected = ''
                  this.level4Selected = ''
                  this.level5Selected = ''
                  this.level3Options = this.rowDataCache.filter(t => t.projectName === this.projectSelected && t.categoryLevel1 === this.level1Selected && t.categoryLevel2 === this.level2Selected).map(t => t.categoryLevel3).filter((value, index, self) => self.indexOf(value) === index)
                  this.level4Options = []
                  this.level5Options = []
                  break
                case 4:
                  this.level4Selected = ''
                  this.level5Selected = ''
                  this.level4Options = this.rowDataCache.filter(t => t.projectName === this.projectSelected && t.categoryLevel1 === this.level1Selected && t.categoryLevel2 === this.level2Selected && t.categoryLevel3 === this.level3Selected).map(t => t.categoryLevel4).filter((value, index, self) => self.indexOf(value) === index)
                  this.level5Options = []
                  break
                case 5:
                  this.level5Selected = ''
                  this.level5Options = this.rowDataCache.filter(t => t.projectName === this.projectSelected && t.categoryLevel1 === this.level1Selected && t.categoryLevel2 === this.level2Selected && t.categoryLevel3 === this.level3Selected && t.categoryLevel4 === this.level4Selected).map(t => t.categoryLevel5).filter((value, index, self) => self.indexOf(value) === index)
                  break
              }
              this.filterData()
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
                  updateCategoryAndManufactoryIdForTasks(values)
                  .then(res => {
                    this.visible = false
                    this.confirmLoading = false
                    // 重置表单数据
                    form.resetFields()
                    // 刷新表格
                    this.reloadData()
                    this.$message.info('修改成功')
                  })
                } else {
                  this.confirmLoading = false
                }
              })
            }
        },
        beforeMount () {
            this.columnDefs = [
                { headerName: 'id', field: 'id', checkboxSelection: true, width: '150', headerCheckboxSelection: true },
                { headerName: 'Enabled', field: 'enabled', filter: true },
                { headerName: 'Task Status', field: 'taskStatus', filter: true },
                { headerName: 'Status', field: 'status', filter: true },
                { headerName: 'manuf Id', field: 'manufacturerId', width: '100', filter: true },
                { headerName: 'cat Id', field: 'categoryId', width: '100', filter: true },
                { headerName: 'rootId', field: 'rootId', width: '150' },
                { headerName: 'project', field: 'projectName', width: '100', filter: true },
                { headerName: 'L1', field: 'categoryLevel1', filter: true, width: '300' },
                { headerName: 'L2', field: 'categoryLevel2', filter: true, width: '300' },
                { headerName: 'L3', field: 'categoryLevel3', filter: true, width: '300' },
                { headerName: 'L4', field: 'categoryLevel4', filter: true, width: '300' },
                { headerName: 'L5', field: 'categoryLevel5', filter: true, width: '300' },
                { headerName: 'Url', field: 'level_Url', filter: true },
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
