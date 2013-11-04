%import re
<div class="modal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    

    <h3 id="myModalLabel">{{content.title}}</h3>
  </div>
  <div class="modal-body">

    <p>
      %for a in content.comments:
      <!--{{re.sub('<[^<]+?>', '', a.text)}}-->
      {{!a.text}}
      %end for
      </p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div>