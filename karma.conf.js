// Karma configuration
// Generated on Tue Apr 08 2014 12:42:00 GMT+0200 (CEST)

module.exports = function(config) {
    config.set({
        // base path, that will be used to resolve files and exclude
        basePath: '',

        // frameworks to use
        frameworks: ['jasmine'],

        // list of files / patterns to load in the browser
        files: [
            'assets/lib/**/angular.js',
            'assets/lib/**/angular-cookies.js',
            'assets/lib/**/angular-resource.js',
            'assets/lib/**/angular-ui-router.js',

            'assets/lib/angular-mocks/angular-mocks.js',

            'ployst/**/static/test/**.js',

            'ployst/**/static/app.js',
            'ployst/**/static/**/ployst.*.js',
            'ployst/github/static/github/github-app.js'
        ],

        preprocessors: {
            'ployst/**/js/*.js': 'coverage'
        },

        // list of files to exclude
        exclude: [
        ],

        // test results reporter to use
        // possible values: 'dots', 'progress', 'junit', 'growl', 'coverage'
        reporters: ['progress', 'coverage'],

        // web server port
        port: 9876,

        // enable / disable colors in the output (reporters and logs)
        colors: true,

        // level of logging
        // possible values:
        // config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN ||
        // config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,

        // enable / disable watching file and executing tests whenever any file
        // changes
        autoWatch: true,

        // Start these browsers, currently available:
        // - Chrome
        // - ChromeCanary
        // - Firefox
        // - Opera (install with `npm install karma-opera-launcher`)
        // - Safari (only Mac; has to be installed with `npm install
        //   karma-safari-launcher`)
        // - PhantomJS
        // - IE (only Windows; install with `npm install karma-ie-launcher`)
        browsers: ['PhantomJS'],

        // If browser does not capture in given timeout [ms], kill it
        captureTimeout: 60000,

        // Continuous Integration mode
        // if true, it capture browsers, run tests and exit
        singleRun: false
    });
};
