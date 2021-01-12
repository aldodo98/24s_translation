const configs = {
  production: {
    WEB_API_SERVICES: 'https://haiwa-crawl-func-lab-westeu.azurewebsites.net',
    Scrapyd_Web_Url: 'http://137.116.216.95:5555/'
  },
  development: {
    WEB_API_SERVICES: 'http://localhost:7071',
    Scrapyd_Web_Url: 'http://137.116.216.95:5555/'
  },
  uat: {
    WEB_API_SERVICES: 'https://xshoudai-crawl-func-westeu-uat.azurewebsites.net',
    Scrapyd_Web_Url: 'http://20.56.0.56:5555/'
  }
}
export default configs
