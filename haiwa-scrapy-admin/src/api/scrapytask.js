import request from '@/utils/request'

const api = {
  user: '/user',
  role: '/role',
  rootTask: 'http://localhost:7071/api/RootTask',
  runRootTask: 'http://localhost:7071/api/RunRootTask',
  categoryTreeTask: 'http://localhost:7071/api/CategoryTreeTask',
  enableCategoryTreeTasks: 'http://localhost:7071/api/EnableCategoryTreeTasks',
  updateCategoryAndManufactoryIdForTasks: 'http://localhost:7071/api/UpdateCategoryAndManufactoryIdForTasks',
  runCategoryTreeTasks: 'http://localhost:7071/api/RunCategoryTreeTasks',
  productTask: 'http://localhost:7071/api/ProductTask',
  enableProductTasks: 'http://localhost:7071/api/EnableProductTasks',
  runProductTasks: 'http://localhost:7071/api/RunProductTasks',
  permission: '/permission',
  permissionNoPager: '/permission/no-pager',
  orgTree: '/org/tree'
}

export default api

export function getSpiderRootTaskList (parameter) {
    return request({
      url: api.rootTask,
      method: 'get'
    })
  }
// id == 0 add     post
// id != 0 update  put
export function saveSpiderRootTask (parameter) {
  return request({
    url: api.rootTask,
    method: parameter.id === 0 ? 'post' : 'put',
    data: parameter
  })
}

export function deleteSpiderRootTask (parameter) {
  return request({
    url: api.rootTask + '/' + parameter.id,
    method: 'delete'
  })
}

export function runSpiderRootTask (parameter) {
  return request({
    url: api.runRootTask + '/' + parameter.id,
    method: 'get'
  })
}

export function getSpiderCategoryTreeTasksList (parameter) {
  return request({
    url: api.categoryTreeTask,
    method: 'get'
  })
}

export function enableSpiderCategoryTreeTasksList (parameter) {
  return request({
    url: api.enableCategoryTreeTasks,
    method: 'post',
    data: parameter
  })
}

export function disableSpiderCategoryTreeTasksList (parameter) {
  return request({
    url: api.enableCategoryTreeTasks,
    method: 'post',
    data: parameter
  })
}

export function updateCategoryAndManufactoryIdForTasks (parameter) {
  return request({
    url: api.updateCategoryAndManufactoryIdForTasks,
    method: 'post',
    data: parameter
  })
}

export function runCategoryTreeTasks (parameter) {
  return request({
    url: api.runCategoryTreeTasks,
    method: 'post',
    data: parameter
  })
}

export function getProductTasksList (parameter) {
  return request({
    url: api.productTask,
    method: 'get'
  })
}

export function enableProductTasksList (parameter) {
  return request({
    url: api.enableProductTasks,
    method: 'post',
    data: parameter
  })
}

export function runProductTasks (parameter) {
  return request({
    url: api.runProductTasks,
    method: 'post',
    data: parameter
  })
}
