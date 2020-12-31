import request from '@/utils/request'
import configs from '@/config/env'

let BACKEND_API_BASE_URL = configs.production.WEB_API_SERVICES
const NODE_ENV = process.env.NODE_ENV
if (NODE_ENV === 'uat') {
  BACKEND_API_BASE_URL = configs.uat.WEB_API_SERVICES
}

const api = {
  user: '/user',
  role: '/role',
  rootTask: BACKEND_API_BASE_URL + '/api/RootTask',
  runRootTask: BACKEND_API_BASE_URL + '/api/RunRootTask',
  categoryTreeTask: BACKEND_API_BASE_URL + '/api/CategoryTreeTask',
  enableCategoryTreeTasks: BACKEND_API_BASE_URL + '/api/EnableCategoryTreeTasks',
  updateCategoryAndManufactoryIdForTasks: BACKEND_API_BASE_URL + '/api/UpdateCategoryAndManufactoryIdForTasks',
  runCategoryTreeTasks: BACKEND_API_BASE_URL + '/api/RunCategoryTreeTasks',
  productTask: BACKEND_API_BASE_URL + '/api/ProductTask',
  enableProductTasks: BACKEND_API_BASE_URL + '/api/EnableProductTasks',
  runProductTasks: BACKEND_API_BASE_URL + '/api/RunProductTasks',
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
