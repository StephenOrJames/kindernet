var del  = require("del");
var gulp = require("gulp");
var $    = require("gulp-load-plugins")();

var paths = {
  dist: "dist",
  scripts: [
    // Libraries required by Foundation
    "bower_components/jquery/dist/jquery.js",
    "bower_components/what-input/what-input.js",
    // Core Foundation files
	"bower_components/foundation-sites/js/foundation.core.js",
    "bower_components/foundation-sites/js/foundation.util.*.js",
    // Individual Foundation components
    "bower_components/foundation-sites/js/foundation.abide.js",
    "bower_components/foundation-sites/js/foundation.accordion.js",
    "bower_components/foundation-sites/js/foundation.accordionMenu.js",
    "bower_components/foundation-sites/js/foundation.drilldown.js",
    "bower_components/foundation-sites/js/foundation.dropdown.js",
    "bower_components/foundation-sites/js/foundation.dropdownMenu.js",
    "bower_components/foundation-sites/js/foundation.equalizer.js",
    "bower_components/foundation-sites/js/foundation.interchange.js",
    "bower_components/foundation-sites/js/foundation.magellan.js",
    "bower_components/foundation-sites/js/foundation.offcanvas.js",
    "bower_components/foundation-sites/js/foundation.orbit.js",
    "bower_components/foundation-sites/js/foundation.responsiveMenu.js",
    "bower_components/foundation-sites/js/foundation.responsiveToggle.js",
    "bower_components/foundation-sites/js/foundation.reveal.js",
    "bower_components/foundation-sites/js/foundation.slider.js",
    "bower_components/foundation-sites/js/foundation.sticky.js",
    "bower_components/foundation-sites/js/foundation.tabs.js",
    "bower_components/foundation-sites/js/foundation.toggler.js",
    "bower_components/foundation-sites/js/foundation.tooltip.js",
    // Project's files
    "src/js/!(app).js",
    "src/js/app.js"
  ],
  styles: [
    "bower_components/foundation-sites/scss",
    "bower_components/motion-ui/src",
    "src/scss"
  ]
}

gulp.task("cleanup", function() {
  return del(paths.dist);
});

gulp.task("images", function() {
  return gulp.src("src/img/**/*")
    .pipe($.imagemin({
      progressive: true
	}))
    .pipe(gulp.dest(paths.dist + "/img"));
});

gulp.task("scripts", function() {
  return gulp.src(paths.scripts)
    .pipe($.babel())
    .pipe($.concat("app.js"))
    .pipe($.uglify()
      .on("error", e => { console.log(e); })
    )
    .pipe(gulp.dest(paths.dist + "/js"));
});

gulp.task("styles", function() {
  return gulp.src("src/scss/app.scss")
    .pipe($.sass({
      includePaths: paths.styles,
        outputStyle: "compressed"
      })
      .on("error", $.sass.logError)
    )
    .pipe($.autoprefixer({
        browsers: ["last 2 versions", "ie >= 9", "and_chr >= 2.3"]
    }))
    .pipe(gulp.dest(paths.dist + "/css"));
});

gulp.task("default", ["cleanup"], function() {
  gulp.run(["images", "scripts", "styles"]);
  gulp.watch(["src/img/**/*"], ["images"]);
  gulp.watch(["src/scss/**/*.scss"], ["styles"]);
  gulp.watch(["src/js/**/*.js"], ["scripts"]);
});
