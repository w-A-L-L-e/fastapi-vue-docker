const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  pluginOptions: {
    i18n: {
      locale: 'nl',
      fallbackLocale: 'nl',
      localeDir: 'locales',
      enableInSFC: false,
      enableBridge: false
    }
  }
})
