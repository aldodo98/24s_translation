// eslint-disable-next-line
import { UserLayout, BasicLayout, BlankLayout } from '@/layouts'
import { bxAnaalyse } from '@/core/icons'
import configs from '@/config/env'

const RouteView = {
  name: 'RouteView',
  render: (h) => h('router-view')
}

export const asyncRouterMap = [

  {
    path: '/',
    name: 'index',
    component: BasicLayout,
    meta: { title: 'menu.home' },
    redirect: '/scrapyadmin/RootTask',
    children: [
      // scrapyadmin
      {
        path: '/scrapyadmin',
        name: 'scrapyadmin',
        redirect: '/scrapyadmin/RootTask',
        component: RouteView,
        meta: { title: 'Spider Admin', keepAlive: true, icon: bxAnaalyse },
        children: [
          {
            path: '/scrapyadmin/RootTask',
            name: 'RootTaskTableListWrapper',
            hideChildrenInMenu: true, // 强制显示 MenuItem 而不是 SubMenu
            component: () => import('@/views/scrapyadmin/RootTask'),
            // component: () => import('@/views/list/TableList'),
            meta: { title: 'SpiderRootTasks', keepAlive: true }
          },
          {
            path: '/scrapyadmin/CategoryTreeTask',
            name: 'CategoryTreeTaskTableListWrapper',
            hideChildrenInMenu: true, // 强制显示 MenuItem 而不是 SubMenu
            component: () => import('@/views/scrapyadmin/CategoryTreeTask'),
            meta: { title: 'SpiderCategoryTreeTasks', keepAlive: true }
          },
          {
            path: '/scrapyadmin/ProductTask',
            name: 'ProductTaskTableListWrapper',
            hideChildrenInMenu: true, // 强制显示 MenuItem 而不是 SubMenu
            component: () => import('@/views/scrapyadmin/ProductTask'),
            meta: { title: 'SpiderProductTasks', keepAlive: true }
          }
        ]
      },
       // 外部链接
      {
        path: configs.production.Scrapyd_Web_Url,
        name: 'Scrapyd Server Monitor',
        meta: { title: 'Scrapyd Server Monitor', target: '_blank' }
      }
    ]
  },
  {
    path: '*', redirect: '/404', hidden: true
  }
]

/**
 * 基础路由
 * @type { *[] }
 */
export const constantRouterMap = [
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/login',
    hidden: true,
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Login')
      },
      {
        path: 'register',
        name: 'register',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Register')
      },
      {
        path: 'register-result',
        name: 'registerResult',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/RegisterResult')
      },
      {
        path: 'recover',
        name: 'recover',
        component: undefined
      }
    ]
  },

  {
    path: '/404',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404')
  }

]
