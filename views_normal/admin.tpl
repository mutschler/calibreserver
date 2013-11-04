<!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="de"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="de"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="de"> <![endif]-->
<!-- Consider adding a manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!--> <html class="no-js" lang="de"> <!--<![endif]-->
<head>
  <meta charset="utf-8">

  <!-- Use the .htaccess and remove these lines to avoid edge case issues.
       More info: h5bp.com/i/378 -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title></title>
  <meta name="description" content="">

  <!-- Mobile viewport optimized: h5bp.com/viewport -->
  <meta name="viewport" content="width=device-width">

  <!-- Place favicon.ico and apple-touch-icon.png in the root directory: mathiasbynens.be/notes/touch-icons -->
  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/css/bootstrap-responsive.min.css">
  <link rel="stylesheet" href="/static/css/style.css">

  <!-- More ideas for your <head> here: h5bp.com/d/head-Tips -->

  <!--[if lt IE 9]>
      <script src="js/libs/html5.js"></script>
  <![endif]-->

  <!-- All JavaScript at the bottom, except this Modernizr build.
       Modernizr enables HTML5 elements & feature detects for optimal performance.
       Create your own custom Modernizr build: www.modernizr.com/download/ 
  <script src="/static/views/js/libs/modernizr-2.6.2.min.js"></script>-->
</head>
<body>
<div class="modal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="display:none">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Modal header</h3>
  </div>
  <div class="modal-body">
    <p>One fine body…</p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
    <button class="btn btn-primary">Save changes</button>
  </div>
</div>
  <!-- Prompt IE 6 users to install Chrome Frame. Remove this if you support IE 6.
       chromium.org/developers/how-tos/chrome-frame-getting-started -->
  <!--[if lt IE 7]><p class=chromeframe>Your browser is <em>ancient!</em> <a href="http://browsehappy.com/">Upgrade to a different browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">install Google Chrome Frame</a> to experience this site.</p><![endif]-->
  <header>
<div class="navbar">
  <div class="navbar-inner">
    <a class="brand" href="#">CalibreServer</a>
    <ul class="nav">
      <li class="active"><a href="/">Home</a></li>
      <li><a href="/authors">Author List</a></li>
      <li><a href="#">Link</a></li>
    </ul>
  <div class="pull-right">
    <form action="/search" method="POST" class="navbar-search pull-left">
      <select name="searchtype" id="searchtype" class="span1">
        <option value="authors">Author</option>
        <option value="description">Description</option>
        <option value="title">Title</option>
      </select>

      <input name="searchfor" id="searchfor" type="text" class="search-query" placeholder="Search">
    </form>
  </div>
  </div>
</div>
  </header>
  <div role="main">
  <div class="container">
    <form class="form-horizontal">
      <legend>Settings</legend>
      <div class="control-group">
        <label class="control-label" for="username">Username</label>
        <div class="controls">
          <input type="text" id="username" name="username" value="{{content.USER}}">
        </div>
      </div>
      <div class="control-group">
        <label class="control-label" for="password">Password</label>
        <div class="controls">
          <input type="password" id="password" name="password" value="{{content.PASS}}">
        </div>
      </div>
      <div class="control-group">
        <label class="control-label" for="port">Port</label>
        <div class="controls">
          <input type="text" id="port" name="port" value="{{content.PORT}}">
        </div>
      </div>
      <div class="control-group">
        <label class="control-label" for="dbroot">Database Root</label>
        <div class="controls">
          <input type="text" id="dbroot" name="dbroot" value="{{content.DB_ROOT}}">
        </div>
      </div>
      <div class="control-group">
        <label class="control-label" for="newbooks">Books on Start Page</label>
        <div class="controls">
          <input type="text" id="newbooks" name="newbooks" value="{{content.NEWEST_BOOKS}}">
        </div>
      </div>
      <div class="control-group">
        <label class="control-label" for="allbooks">Books on Book Page</label>
        <div class="controls">
          <input type="text" id="allbooks" name="allbooks" value="{{content.ALL_BOOKS}}">
        </div>
      </div>
      <div class="control-group">
        <label class="control-label" for="webadmin">Web admin interface</label>
        <div class="controls">
          <input type="checkbox" id="webadmin" name="webadmin" checked="{{content.WEB_ADMIN}}">
        </div>
      </div>
      <div class="control-group">
        <div class="controls">
          <a type="button" id="saveChanges" class="btn">Save Changes</a>
        </div>
      </div>
    </form>

  </div>
  </div>
  <footer>

  </footer>


  <!-- JavaScript at the bottom for fast page loading -->

  <!-- Grab Google CDN's jQuery, with a protocol relative URL; fall back to local if offline -->
  <script src="/static/js/libs/jquery-1.8.1.min.js"></script>

  <!-- scripts concatenated and minified via build script -->
  <script src="/static/js/bootstrap.min.js"></script>
  <script type="text/javascript">
  $("#saveChanges").click(function(){
    $(this).text("Saving...");
    var data = $("form :input").serialize();
    //alert(data);
    $.ajax({
                type: "POST",
                url: "/admin/save",
                data: data,
                success: function(){
                  $("#saveChanges").text("Saved").addClass("btn-success");
                }
            });
  })
  </script>
  <!-- end scripts -->


</body>
</html>

