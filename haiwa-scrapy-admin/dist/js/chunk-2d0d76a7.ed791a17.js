(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0d76a7"],{"775f":function(e,t,l){"use strict";l.r(t);var a=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticStyle:{width:"100%",flex:"1 1 auto"}},[l("page-header-wrapper",{staticStyle:{"padding-bottom":"5px"}},[l("a-card",{attrs:{bordered:!1}},[l("div",{staticClass:"table-page-search-wrapper"},[l("a-form",{attrs:{layout:"inline"}},[l("a-row",{attrs:{gutter:48}},[l("a-col",{attrs:{md:4,sm:24}},[l("a-form-item",{attrs:{label:"Enabled"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:e.filterData},model:{value:e.isEnabled,callback:function(t){e.isEnabled=t},expression:"isEnabled"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),l("a-select-option",{attrs:{value:"true"}},[e._v("true")]),l("a-select-option",{attrs:{value:"false"}},[e._v("false")])],1)],1)],1),l("a-col",{attrs:{md:4,sm:24}},[l("a-form-item",{attrs:{label:"TaskStatus"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:e.filterData},model:{value:e.taskStatus,callback:function(t){e.taskStatus=t},expression:"taskStatus"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),l("a-select-option",{attrs:{value:"Waiting"}},[e._v("Waiting")]),l("a-select-option",{attrs:{value:"Prepare"}},[e._v("Prepare")]),l("a-select-option",{attrs:{value:"Finish"}},[e._v("Finish")]),l("a-select-option",{attrs:{value:"Trigered"}},[e._v("Trigered")])],1)],1)],1),l("a-col",{attrs:{md:4,sm:24}},[l("a-form-item",{attrs:{label:"Status"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:e.filterData},model:{value:e.status,callback:function(t){e.status=t},expression:"status"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),l("a-select-option",{attrs:{value:"New"}},[e._v("New")]),l("a-select-option",{attrs:{value:"Deleted"}},[e._v("Deleted")]),l("a-select-option",{attrs:{value:"Active"}},[e._v("Active")]),l("a-select-option",{attrs:{value:"Changed"}},[e._v("Changed")])],1)],1)],1),l("a-col",{attrs:{md:4,sm:24}},[l("a-form-item",{attrs:{label:"Project"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:function(t){return e.loadLevelOption(1)}},model:{value:e.projectSelected,callback:function(t){e.projectSelected=t},expression:"projectSelected"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),e._l(e.projectOptions,(function(t){return l("a-select-option",{key:t},[e._v(" "+e._s(t)+" ")])}))],2)],1)],1),l("a-col",{attrs:{md:6,sm:24}},[l("a-form-item",{attrs:{label:"L1"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:function(t){return e.loadLevelOption(2)}},model:{value:e.level1Selected,callback:function(t){e.level1Selected=t},expression:"level1Selected"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),e._l(e.level1Options,(function(t){return l("a-select-option",{key:t},[e._v(" "+e._s(t)+" ")])}))],2)],1)],1),l("a-col",{attrs:{md:6,sm:24}},[l("a-form-item",{attrs:{label:"L2"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:function(t){return e.loadLevelOption(3)}},model:{value:e.level2Selected,callback:function(t){e.level2Selected=t},expression:"level2Selected"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),e._l(e.level2Options,(function(t){return l("a-select-option",{key:t},[e._v(" "+e._s(t)+" ")])}))],2)],1)],1),l("a-col",{attrs:{md:6,sm:24}},[l("a-form-item",{attrs:{label:"L3"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:function(t){return e.loadLevelOption(4)}},model:{value:e.level3Selected,callback:function(t){e.level3Selected=t},expression:"level3Selected"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),e._l(e.level3Options,(function(t){return l("a-select-option",{key:t},[e._v(" "+e._s(t)+" ")])}))],2)],1)],1),l("a-col",{attrs:{md:6,sm:24}},[l("a-form-item",{attrs:{label:"L4"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:function(t){return e.loadLevelOption(5)}},model:{value:e.level4Selected,callback:function(t){e.level4Selected=t},expression:"level4Selected"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),e._l(e.level4Options,(function(t){return l("a-select-option",{key:t},[e._v(" "+e._s(t)+" ")])}))],2)],1)],1),l("a-col",{attrs:{md:6,sm:24}},[l("a-form-item",{attrs:{label:"L5"}},[l("a-select",{attrs:{placeholder:"请选择","default-value":""},on:{change:e.filterData},model:{value:e.level5Selected,callback:function(t){e.level5Selected=t},expression:"level5Selected"}},[l("a-select-option",{attrs:{value:""}},[e._v("全部")]),e._l(e.level5Options,(function(t){return l("a-select-option",{key:t},[e._v(" "+e._s(t)+" ")])}))],2)],1)],1)],1)],1)],1)])],1),l("button",{on:{click:function(t){return e.enableSelectedRows()}}},[e._v("Enable Selected Rows")]),l("button",{on:{click:function(t){return e.disableSelectedRows()}}},[e._v("Disable Selected Rows")]),l("button",{on:{click:function(t){return e.updateSelectedRows()}}},[e._v("Update Category & MenufactoryId for Selected Rows")]),l("button",{on:{click:function(t){return e.runSelectedRows()}}},[e._v("Run Selected Rows")]),l("ag-grid-vue",{staticClass:"ag-theme-alpine",staticStyle:{width:"99%",height:"500px"},attrs:{columnDefs:e.columnDefs,rowData:e.rowData,defaultColDef:e.defaultColDef,rowSelection:"multiple"},on:{"grid-ready":e.onGridReady}}),l("div",{staticClass:"ag-status-name-value"},[l("span",[e._v("Row Count :")]),l("span",[e._v(e._s(e.count))])]),l("udpate-form",{ref:"UpdateCategoryAndMenuIdForm",attrs:{visible:e.visible,loading:e.confirmLoading,model:e.mdl},on:{cancel:e.handleCancel,ok:e.handleOk}})],1)},n=[],i=(l("4de4"),l("c975"),l("d81d"),l("d3b7"),l("25f0"),l("401b")),o=l("5ed6"),r=l("c189"),s={name:"CategoryTreeTask",data:function(){return{projectOptions:[],level1Options:[],level2Options:[],level3Options:[],level4Options:[],level5Options:[],projectSelected:"",level1Selected:"",level2Selected:"",level3Selected:"",level4Selected:"",level5Selected:"",isEnabled:"",taskStatus:"",status:"",visible:!1,confirmLoading:!1,mdl:null,columnDefs:null,rowDataCache:null,rowData:null,gridApi:null,columnApi:null,defaultColDef:null,autoGroupColumnDef:null,count:0}},components:{AgGridVue:i["AgGridVue"],"udpate-form":r["a"]},methods:{filterData:function(){var e=this,t=this.rowDataCache;"true"===this.isEnabled&&(t=t.filter((function(e){return e.enabled}))),"false"===this.isEnabled&&(t=t.filter((function(e){return!1===e.enabled}))),""!==this.taskStatus&&(t=t.filter((function(t){return t.taskStatus===e.taskStatus}))),""!==this.status&&(t=t.filter((function(t){return t.status===e.status}))),""!==this.projectSelected&&(t=t.filter((function(t){return t.projectName===e.projectSelected}))),""!==this.level1Selected&&(t=t.filter((function(t){return t.categoryLevel1===e.level1Selected}))),""!==this.level2Selected&&(t=t.filter((function(t){return t.categoryLevel2===e.level2Selected}))),""!==this.level3Selected&&(t=t.filter((function(t){return t.categoryLevel3===e.level3Selected}))),""!==this.level4Selected&&(t=t.filter((function(t){return t.categoryLevel4===e.level4Selected}))),""!==this.level5Selected&&(t=t.filter((function(t){return t.categoryLevel5===e.level5Selected}))),this.rowData=t,this.count=t.length},onGridReady:function(e){this.gridApi=e.api,this.columnApi=e.columnApi},getSelectedTaskIds:function(){var e=this.gridApi.getSelectedNodes(),t=e.map((function(e){return e.data})),l=t.map((function(e){return e.id}));return l},enableSelectedRows:function(){var e=this,t=this.getSelectedTaskIds(),l={TaskIds:t,Enable:!0};Object(o["d"])(l).then((function(t){e.confirmLoading=!1,e.reloadData(),e.$message.info("enable 成功")}))},disableSelectedRows:function(){var e=this,t=this.getSelectedTaskIds(),l={TaskIds:t,Enable:!1};Object(o["b"])(l).then((function(t){e.confirmLoading=!1,e.reloadData(),e.$message.info("disable 成功")}))},updateSelectedRows:function(){var e=this.getSelectedTaskIds();e.length>0?(this.mdl={TaskIds:e.toString()},this.visible=!0):this.$message.warning("You need to select the rows to update")},runSelectedRows:function(){var e=this,t=this.getSelectedTaskIds();if(t.length>0){var l={TaskIds:t.toString()};Object(o["h"])(l).then((function(t){e.confirmLoading=!1,e.reloadData(),e.$message.info("disable 成功")}))}else this.$message.warning("You need to select the rows to run")},reloadData:function(){var e=this;Object(o["f"])().then((function(t){e.rowDataCache=t,e.projectOptions=t.map((function(e){return e.projectName})).filter((function(e,t,l){return l.indexOf(e)===t})),e.filterData()}))},loadLevelOption:function(e){var t=this;switch(e){case 1:this.level1Selected="",this.level2Selected="",this.level3Selected="",this.level4Selected="",this.level5Selected="",this.level1Options=this.rowDataCache.filter((function(e){return e.projectName===t.projectSelected})).map((function(e){return e.categoryLevel1})).filter((function(e,t,l){return l.indexOf(e)===t})),this.level2Options=[],this.level3Options=[],this.level4Options=[],this.level5Options=[];break;case 2:this.level2Selected="",this.level3Selected="",this.level4Selected="",this.level5Selected="",this.level2Options=this.rowDataCache.filter((function(e){return e.projectName===t.projectSelected&&e.categoryLevel1===t.level1Selected})).map((function(e){return e.categoryLevel2})).filter((function(e,t,l){return l.indexOf(e)===t})),this.level3Options=[],this.level4Options=[],this.level5Options=[];break;case 3:this.level3Selected="",this.level4Selected="",this.level5Selected="",this.level3Options=this.rowDataCache.filter((function(e){return e.projectName===t.projectSelected&&e.categoryLevel1===t.level1Selected&&e.categoryLevel2===t.level2Selected})).map((function(e){return e.categoryLevel3})).filter((function(e,t,l){return l.indexOf(e)===t})),this.level4Options=[],this.level5Options=[];break;case 4:this.level4Selected="",this.level5Selected="",this.level4Options=this.rowDataCache.filter((function(e){return e.projectName===t.projectSelected&&e.categoryLevel1===t.level1Selected&&e.categoryLevel2===t.level2Selected&&e.categoryLevel3===t.level3Selected})).map((function(e){return e.categoryLevel4})).filter((function(e,t,l){return l.indexOf(e)===t})),this.level5Options=[];break;case 5:this.level5Selected="",this.level5Options=this.rowDataCache.filter((function(e){return e.projectName===t.projectSelected&&e.categoryLevel1===t.level1Selected&&e.categoryLevel2===t.level2Selected&&e.categoryLevel3===t.level3Selected&&e.categoryLevel4===t.level4Selected})).map((function(e){return e.categoryLevel5})).filter((function(e,t,l){return l.indexOf(e)===t}));break}this.filterData()},handleCancel:function(){this.visible=!1;var e=this.$refs.UpdateCategoryAndMenuIdForm.form;e.resetFields()},handleOk:function(){var e=this,t=this.$refs.UpdateCategoryAndMenuIdForm.form;this.confirmLoading=!0,t.validateFields((function(l,a){l?e.confirmLoading=!1:Object(o["l"])(a).then((function(l){e.visible=!1,e.confirmLoading=!1,t.resetFields(),e.reloadData(),e.$message.info("修改成功")}))}))}},beforeMount:function(){this.columnDefs=[{headerName:"id",field:"id",checkboxSelection:!0,width:"150",headerCheckboxSelection:!0},{headerName:"Enabled",field:"enabled",filter:!0},{headerName:"Task Status",field:"taskStatus",filter:!0},{headerName:"Status",field:"status",filter:!0},{headerName:"manuf Id",field:"manufacturerId",width:"100",filter:!0},{headerName:"cat Id",field:"categoryId",width:"100",filter:!0},{headerName:"rootId",field:"rootId",width:"150"},{headerName:"project",field:"projectName",width:"100",filter:!0},{headerName:"L1",field:"categoryLevel1",filter:!0,width:"300"},{headerName:"L2",field:"categoryLevel2",filter:!0,width:"300"},{headerName:"L3",field:"categoryLevel3",filter:!0,width:"300"},{headerName:"L4",field:"categoryLevel4",filter:!0,width:"300"},{headerName:"L5",field:"categoryLevel5",filter:!0,width:"300"},{headerName:"Url",field:"level_Url",filter:!0},{headerName:"Create",field:"createDateTime"},{headerName:"Update",field:"updateDateTime"}],this.defaultColDef={resizable:!0},this.autoGroupColumnDef={headerName:"Model",field:"model",cellRenderer:"agGroupCellRenderer",cellRendererParams:{checkbox:!0}},this.reloadData()}},c=s,d=l("2877"),u=Object(d["a"])(c,a,n,!1,null,null,null);t["default"]=u.exports}}]);