module.exports = function(grunt){
    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        concat: {
        },

        less: {
            development: {
                files: {
                    "rynda/static/css/rynda-theme.css": "less/rynda-theme.less",
                    "rynda/static/css/rynda.css": "less/rynda.less"    
                }
            }
        },

        jshint: {
            all: ["Gruntfile.js"]
        }
    });

    grunt.loadNpmTasks("grunt-contrib-concat");
    grunt.loadNpmTasks("grunt-contrib-jshint");
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.registerTask("default", ["jshint"]);
};
