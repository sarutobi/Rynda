module.exports = function(grunt){
    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        concat: {
        },

        // Build css from less styles
        less: {
            development: {
                files: {
                    // "rynda/static/css/bootstrap.css": "assets/css/bootstrap/bootstrap.less",
                    "rynda/static/css/bootstrap-theme.css": "assets/css/rynda-theme.less",
                    "rynda/static/css/default.css": "assets/css/rynda.less"    
                }
            }
        },

        // Check javascripts
        jshint: {
            all: ["Gruntfile.js", "assets/javascripts/*.js"]
        },

        // Copying files
        copy: {
            // Libraries
            libs: {
                files: [
                    {expand: true, cwd:"assets/javascript/", src:["libs/*.js"], dest: "rynda/static/js/"},
                ]},

            // Development javascripts
            sourcejs: {
                files:[
                    {expand: true, cwd:"assets/javascript/", src:["*.js"], dest: "rynda/static/js/", filter: "isFile"} 
                ]},

            // Css files
            css: {
                files: [
                    {expand: true, cwd:"assets/css/", src:["*.css"], dest: "rynda/static/css/", filter: "isFile"} 
                ]}
        },

        // Clean destination dirs
        clean: ["rynda/static/js", "rynda/static/css"]
    });

    grunt.loadNpmTasks("grunt-contrib-concat");
    grunt.loadNpmTasks("grunt-contrib-jshint");
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.loadNpmTasks("grunt-contrib-clean");
    grunt.registerTask("default", ["jshint", "copy:libs"]);
    grunt.registerTask("develop", ["jshint", "clean", "less:development", "copy:libs", "copy:sourcejs", "copy:css"]);
};
