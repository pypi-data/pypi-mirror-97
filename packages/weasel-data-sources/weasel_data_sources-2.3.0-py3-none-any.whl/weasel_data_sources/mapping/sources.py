""" Includes a set of known data sources """

SOURCES = {
    "All in One SEO Pack": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:semperfiwebdesign:all_in_one_seo_pack",
        "git": "https://github.com/awesomemotive/all-in-one-seo-pack",
    },
    "Angular": {
        "cdnjs": "angular",
        "cpe": None,
        "git": "https://github.com/angular/angular",
    },
    "AngularJS": {
        "cdnjs": "angular.js",
        "cpe": "cpe:2.3:a:angularjs:angular.js",
        "git": "https://github.com/angular/angular.js.git",
    },
    "animate.css": {
        "cdnjs": "animate.css",
        "cpe": None,
        "git": "https://github.com/animate-css/animate.css",
    },
    "Axios": {
        "cdnjs": "axios",
        "cpe": "cpe:2.3:a:axios:axios",
        "git": "https://github.com/axios/axios",
    },
    "Backbone.js": {
        "cdnjs": "backbone.js",
        "cpe": "cpe:2.3:a:backbone_project:backbone",
        "git": "https://github.com/jashkenas/backbone.git",
    },
    "Bootstrap": {
        "cdnjs": "twitter-bootstrap",
        "cpe": "cpe:2.3:a:getbootstrap:bootstrap",
        "git": "https://github.com/twbs/bootstrap",
    },
    "CKEditor": {
        "cdnjs": "ckeditor",
        "cpe": "cpe:2.3:a:ckeditor:ckeditor",
        "git": "https://github.com/ckeditor/ckeditor-dev.git",
    },
    "Concrete5": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:concrete5:concrete5",
        "git": "https://github.com/concrete5/concrete5",
    },
    "D3": {
        "cdnjs": "d3",
        "cpe": "cpe:2.3:a:d3.js_project:d3.js",
        "git": "https://github.com/d3/d3.git",
    },
    "Discourse": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:discourse:discourse",
        "git": "https://github.com/discourse/discourse",
    },
    "Drupal": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:drupal:drupal",
        "git": "https://git.drupalcode.org/project/drupal.git",
    },
    "Ember.js": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:emberjs:ember.js",
        "git": "https://github.com/emberjs/ember.js",
    },
    "ExtJS": {"cdnjs": "extjs", "cpe": None, "git": None},
    "FancyBox": {
        "cdnjs": "fancybox",
        "cpe": None,
        "git": "https://github.com/fancyapps/fancybox",
    },
    "Flask": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:palletsprojects:flask",
        "git": "https://github.com/pallets/flask",
    },
    "Font Awesome": {
        "cdnjs": "font-awesome",
        "cpe": None,
        "git": "https://github.com/FortAwesome/Font-Awesome.git",
    },
    "Hammer.js": {
        "cdnjs": "hammer.js",
        "cpe": None,
        "git": "https://github.com/hammerjs/hammer.js.git",
    },
    "Handlebars": {
        "cdnjs": "handlebars.js",
        "cpe": "cpe:2.3:a:handlebars.js_project:handlebars.js",
        "git": "https://github.com/wycats/handlebars.js",
    },
    "Highcharts": {
        "cdnjs": "highcharts",
        "cpe": None,
        "git": "https://github.com/highcharts/highcharts.git",
    },
    "Joomla": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:joomla:joomla\\!",
        "git": "https://github.com/joomla/joomla-cms",
    },
    "Knockout.js": {
        "cdnjs": "knockout",
        "cpe": "cpe:2.3:a:knockoutjs:knockout",
        "git": "https://github.com/knockout/knockout.git",
    },
    "Lodash": {
        "cdnjs": "lodash.js",
        "cpe": "cpe:2.3:a:lodash:lodash",
        "git": "https://github.com/lodash/lodash.git",
    },
    "MathJax": {
        "cdnjs": "mathjax",
        "cpe": "cpe:2.3:a:mathjax:mathjax",
        "git": "https://github.com/mathjax/MathJax",
    },
    "MediaElement.js": {
        "cdnjs": "mediaelement",
        "cpe": "cpe:2.3:a:mediaelementjs:mediaelement.js",
        "git": "https://github.com/mediaelement/mediaelement",
    },
    "MediaWiki": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:mediawiki:mediawiki",
        "git": "https://github.com/wikimedia/mediawiki",
    },
    "Modernizr": {
        "cdnjs": None,
        "cpe": None,
        "git": "https://github.com/Modernizr/Modernizr",
    },
    "Moment.js": {
        "cdnjs": "moment.js",
        "cpe": "cpe:2.3:a:momentjs:moment",
        "git": "https://github.com/moment/moment",
    },
    "Mustache": {
        "cdnjs": "mustache.js",
        "cpe": "cpe:2.3:a:mustache.js_project:mustache.js",
        "git": "https://github.com/janl/mustache.js",
    },
    "NextGEN Gallery": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:imagely:nextgen_gallery",
        "git": "https://github.com/wp-plugins/nextgen-gallery",
    },
    "Nextcloud": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:nextcloud:nextcloud_server",
        "git": "https://github.com/nextcloud/server",
    },
    "Phusion Passenger": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:phusionpassenger:phusion_passenger",
        "git": "https://github.com/phusion/passenger",
        "repo_tag_regex": r"release-((?:\d+\.\d+).*)$",
    },
    "Polymer": {
        "cdnjs": "polymer",
        "cpe": None,
        "git": "https://github.com/Polymer/polymer.git",
    },
    "Prototype": {
        "cdnjs": "prototype",
        "cpe": "cpe:2.3:a:prototypejs:prototype_javascript_framework",
        "git": "https://github.com/sstephenson/prototype.git",
    },
    "Raphael": {
        "cdnjs": "raphael",
        "cpe": None,
        "git": "https://github.com/DmitryBaranovskiy/raphael/",
    },
    "React": {
        "cdnjs": "react",
        "cpe": "cpe:2.3:a:facebook:react",
        "git": "https://github.com/facebook/react",
    },
    "RequireJS": {
        "cdnjs": "require.js",
        "cpe": None,
        "git": "https://github.com/jrburke/requirejs",
    },
    "SPIP": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:spip:spip",
        "git": "https://github.com/spip/SPIP",
    },
    "Socket.io": {
        "cdnjs": "socket.io",
        "cpe": None,
        "git": "https://github.com/socketio/socket.io.git",
    },
    "three.js": {
        "cdnjs": "three.js",
        "cpe": None,
        "git": "https://github.com/mrdoob/three.js.git",
        "repo_tag_regex": r"^(r\d+.*)$",
    },
    "TYPO3 CMS": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:typo3:typo3",
        "git": "https://github.com/TYPO3/TYPO3.CMS",
    },
    "TinyMCE": {
        "cdnjs": "tinymce",
        "cpe": None,
        "git": "https://github.com/tinymce/tinymce.git",
    },
    "Underscore.js": {
        "cdnjs": "underscore.js",
        "cpe": None,
        "git": "https://github.com/jashkenas/underscore/",
    },
    "Vue.js": {"cdnjs": "vue", "cpe": None, "git": "https://github.com/vuejs/vue.git"},
    "WP Rocket": {
        "cdnjs": None,
        "cpe": None,
        "git": "https://github.com/wp-media/wp-rocket",
        "repo_tag_regex": r"^(?:v\.?)?((?:\d+\.\d+).*)$",
    },
    "WP-Statistics": {
        "cdnjs": None,
        "cpe": None,
        "git": "https://github.com/wp-statistics/wp-statistics",
    },
    "WooCommerce": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:woocommerce:woocommerce",
        "git": "https://github.com/woocommerce/woocommerce",
    },
    "WordPress": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:wordpress:wordpress",
        "git": None,
        "svn": "https://core.svn.wordpress.org/",
    },
    "XRegExp": {
        "cdnjs": "xregexp",
        "cpe": None,
        "git": "https://github.com/slevithan/XRegExp.git",
    },
    "YUI": {
        "cdnjs": "yui",
        "cpe": "cpe:2.3:a:yahoo:yui",
        "git": "https://github.com/yui/yui3.git",
    },
    "Yoast SEO": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:yoast:wordpress_seo",
        "git": "https://github.com/Yoast/wordpress-seo",
    },
    "ZURB Foundation": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:zurb_foundation:zurb_foundation",
        "git": "https://github.com/foundation/foundation-sites",
    },
    "jQuery": {
        "cdnjs": "jquery",
        "cpe": "cpe:2.3:a:jquery:jquery",
        "git": "https://github.com/jquery/jquery.git",
    },
    "jQuery Migrate": {
        "cdnjs": "jquery-migrate",
        "cpe": None,
        "git": "https://github.com/jquery/jquery-migrate.git",
    },
    "jQuery UI": {
        "cdnjs": "jqueryui",
        "cpe": "cpe:2.3:a:jqueryui:jquery_ui",
        "git": "https://github.com/jquery/jquery-ui",
    },
    "ownCloud": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:owncloud:owncloud",
        "git": "https://github.com/owncloud/core",
    },
    "phpMyAdmin": {
        "cdnjs": None,
        "cpe": "cpe:2.3:a:phpmyadmin:phpmyadmin",
        "git": "https://github.com/phpmyadmin/phpmyadmin",
        "repo_tag_regex": r"^RELEASE_((?:\d+_)*(?:.*))$",
        "repo_tag_substitute": (r"_", "."),
    },
}
