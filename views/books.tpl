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


%for entry in content:


    <div class="row">
      <div class="span2">
        %if entry.has_cover:
        <img src="/download/{{entry.path}}/cover.jpg" />
        %end if
      </div>
      <div class="span10">
        <h1>{{entry.title}}</h1>
        <h3><a href="/authors/{{entry.authors[0].name}}">{{entry.authors[0].name}}</a></h3>
        %if entry.ratings:
        %counter = 0
        Rating:
          %for rating in entry.ratings:
          <a href="/rating/{{rating.rating/2}}">
          %while counter < rating.rating/2:
          <span class="icon-star"></span>
          %counter = counter+1
          %end while
        </a>
          %end for
        %end if
        %if entry.series:
          %for series in entry.series:
            <br />Book {{entry.series_index}} of Series: <a href="/series/{{series.name}}">{{series.name}}</a>
          %end for
        %end if
        %if entry.tags:
        <p><b>Tags:</b>
  %for tag in entry.tags:
    <a href="/tag/{{tag.name}}">{{tag.name}}</a>
  %end for
  </p>
%end if
        <div class="form-actions btn-toolbar">
            %for download in entry.data:
              %if download.format == "EPUB":
                <a class="btn btn-success" href="/download/{{entry.path}}/{{download.name}}.{{download.format.lower()}}">
                 {{download.format}}
                </a>
              %else:
                <a class="btn " href="/download/{{entry.path}}/{{download.name}}.{{download.format.lower()}}">
                 {{download.format}}
                </a>
              %end if
            
             %end for


          <a data-toggle="dafuq" href="/details/{{entry.id}}" data-target="#myModal" class="btn btn-primary">Info</a>
        </div>
       
      </div>
    </div>

%end for

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
  $("a[data-toggle=dafuq]").click(function(event) {
event.preventDefault()
  var target = $(this).attr('data-target');
console.log(target)

  var url = $(this).attr('href');
  $(target).load(url)
$(target).modal('show')
})

  $("#myModal").modal('hide')
  </script>
  <!-- end scripts -->


</body>
</html>

