const gulp = require('gulp')
const cleanDest = require('gulp-clean-dest')
const del = require('del')
const coffee = require('gulp-coffee')
const sourcemaps = require('gulp-sourcemaps')
const coffeelint = require('gulp-coffeelint')
const inject = require('gulp-inject')
const bowerFiles = require('main-bower-files')
const connect = require('gulp-connect')
const runSequence = require('run-sequence')
const ngHtml2Js = require("gulp-ng-html2js")
const concat = require("gulp-concat")
const uglify = require("gulp-uglify")
const cleanCSS = require('gulp-clean-css')
const imagemin  = require('gulp-imagemin')
const less = require('gulp-less')
const flatten = require('gulp-flatten')

// const browserSync = require('browser-sync')

// Variables
const name = "dofus"

const paths = {
  src: 'src',
  dist: 'dist',
  tmp: '.tmp'
}

const src = {
  scripts: paths.src+"/**/*.coffee",
  stylesheets: paths.src+"/**/*.less",
  templates: paths.src+"/**/*_template.html",
  index: paths.src+"/index.html",
  images: paths.src+"/images/*"
}

const dest = {
  all: paths.dist+"/**/*.*",
  scripts: paths.dist+"/js",
  stylesheets: paths.dist+"/css",
  images: paths.dist+"/images",
  tmp: {
    scripts: paths.tmp+"/js",
    templates: paths.tmp+"/templates"
  }
}

const tmp = {
  scripts: [dest.tmp.scripts+"/**/*.js", dest.tmp.templates+"/**/*.js"]
}

var config = {
  host: "localhost",
  port: 9000
  // wiredepIgnorePath: /\.\.\/\.\.\//
}


// clean the contents of the distribution directory
gulp.task('clean', function() {
    return del([paths.dist, paths.tmp])
});

// Watch files changes
gulp.task('watch', function() {
  gulp.watch(src.scripts, ['scripts'])
  gulp.watch(src.templates, ['scripts'])
  gulp.watch(src.stylesheets, ['stylesheets'])
  gulp.watch(src.index, ['index'])
  gulp.watch(src.images, ['images'])
  gulp.watch(dest.all).on('change', connect.reload)
});

// TypeScript compile
gulp.task('compile', function () {
  return gulp
    .src(src.scripts)
    .pipe(cleanDest(dest.tmp.scripts))
    .pipe(coffeelint())
    .pipe(coffeelint.reporter('default'))
    .pipe(sourcemaps.init())
    .pipe(coffee())
    .pipe(gulp.dest(dest.tmp.scripts));
});

// Converting AngularJS templates to Javascript
gulp.task('html2js', function() {
  return gulp
    .src(src.templates)
    .pipe(cleanDest(dest.tmp.templates))
    .pipe(ngHtml2Js({
      moduleName: function(file) {
        pathParts = file.path.split('/')
        folder = "misc."+pathParts[pathParts.length-1]
        return folder.replace('_template.html', 'Template')
      }
    }))
    .pipe(concat("templates.js"))
    .pipe(gulp.dest(dest.tmp.templates))
})

// Concatenate & minify Javascript files
gulp.task('scripts', ['compile', 'html2js'], function() {
  return gulp
    .src(tmp.scripts)
    .pipe(cleanDest(dest.scripts))
    .pipe(sourcemaps.init())
    .pipe(concat(name+".min.js"))
    .pipe(uglify({mangle: false}))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dest.scripts))
})

// Concatenate & Minify CSS files
gulp.task('stylesheets', function() {
  return gulp
    .src(src.stylesheets)
    .pipe(cleanDest(dest.stylesheets))
    .pipe(less())
    .pipe(cleanCSS())
    .pipe(concat(name+".min.css"))
    .pipe(gulp.dest(dest.stylesheets))
})

//
gulp.task('bower:scripts', function() {
  return gulp
    .src(bowerFiles({'filter': '**/*.js'}), {base: 'bower_components'})
    .pipe(concat("bower_components.min.js"))
    .pipe(uglify())
    .pipe(gulp.dest(paths.dist+"/js"))
})

//
gulp.task('bower:less', function() {
  return gulp
    .src(bowerFiles({'filter': '**/*.less'}), {base: 'bower_components'})
    .pipe(less())
    .pipe(cleanCSS())
    .pipe(concat("bower_components_2.min.css"))
    .pipe(gulp.dest(paths.dist+"/css"))
})

//
gulp.task('bower:stylesheets', function() {
  return gulp
    .src(bowerFiles({'filter': '**/*.css'}), {base: 'bower_components'})
    .pipe(concat("bower_components.min.css"))
    .pipe(cleanCSS())
    .pipe(gulp.dest(paths.dist+"/css"))
})

//
gulp.task('bower:fonts', function() {
  return gulp
    .src(bowerFiles({'filter': '**/fonts/*'}), {base: './'})
    .pipe(flatten())
    .pipe(gulp.dest(paths.dist+"/fonts"))
})

// Injecting all files for development
gulp.task('index', ['bower:scripts', 'bower:stylesheets', 'bower:less', 'bower:fonts'], function() {
  return gulp
    .src(src.index)
    .pipe(inject(gulp.src([dest.scripts+"/bower_components.min.js", dest.stylesheets+"/bower_components*.min.css"], {read: false}),
                 {ignorePath: paths.dist, addRootSlash: false, name: 'bower'}))
    .pipe(inject(gulp.src([dest.scripts+"/"+name+".min.js", dest.stylesheets+"/"+name+".min.css"], {read: false}),
                 {ignorePath: paths.dist, addRootSlash: false}))
    .pipe(gulp.dest(paths.dist))
})

// Optimize PNG, JPG, GIF, SVG images with gulp task.
gulp.task('imagemin', function() {
  return gulp
    .src(src.images)
    .pipe(cleanDest(dest.images))
    .pipe(imagemin({ progressive: true }))
    .pipe(gulp.dest(dest.images))
})

//
gulp.task('connect', function() {
  return connect.server({
    livereload: true,
    port: config.port,
    root: [paths.dist+"/index.html", paths.dist]
  })
})


// Tasks
gulp.task('build', function() {
  runSequence('clean', ['scripts', 'stylesheets', 'imagemin'], 'index')
})
gulp.task('server', function() {
    return runSequence('clean', ['scripts', 'stylesheets', 'imagemin'], 'index', ['connect', 'watch']);
})
