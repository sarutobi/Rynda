module.exports = function(grunt){
    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        concat: {
        },

        // Build css from less styles
        less: {
            dev: {
                files: {
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
            // Development version
            dev: {
                files: [
                    // Libraries
                    {expand: true, cwd:"assets/javascript/", src:["libs/*.js"], dest: "rynda/static/js/"},

                    // Development javascripts
                    {expand: true, cwd:"assets/javascript/", src:["*.js"], dest: "rynda/static/js/", filter: "isFile"},

                    // Css files
                    {expand: true, cwd:"assets/css/", src:["*.css"], dest: "rynda/static/css/", filter: "isFile"} 
                ]},

            //Root files
            prod: {
                files:[
                    {src:["*.txt", "README.md", "manage.py"], dest: "build/"},
                    {src:["rynda/**/*.html", "rynda/**/*.json", "rynda/**/*.py" , "!**/tests/**", "!**/test/**"], dest:"build/"},
                    {src:"locale/**/*.po", dest:"build/"}
                ]}
        },

        // Clean destination dirs
        clean: ["build", "rynda/static/js", "rynda/static/css"]
    });

    grunt.loadNpmTasks("grunt-contrib-concat");
    grunt.loadNpmTasks("grunt-contrib-jshint");
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.loadNpmTasks("grunt-contrib-clean");
    grunt.registerTask("default", ["jshint", "clean", "less:dev", "copy:dev"]);
    grunt.registerTask("package", ["jshint", "clean", "less:development", "copy:root", "copy:libs", "copy:sourcejs", "copy:css"]);
};
