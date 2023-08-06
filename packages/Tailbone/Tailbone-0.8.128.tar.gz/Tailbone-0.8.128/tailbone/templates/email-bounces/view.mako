## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

## TODO: this page still uses jQuery but should use Vue.js

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    function autosize_message(scrolldown) {
        var msg = $('#message');
        var height = $(window).height() - msg.offset().top - 50;
        msg.height(height);
        if (scrolldown) {
            msg.animate({scrollTop: msg.get(0).scrollHeight - height}, 250);
        }
    }

    $(function () {
        autosize_message(true);
        $('#message').focus();
    });

    $(window).resize(function() {
        autosize_message(false);
    });

  </script>
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    #message {
        border: 1px solid #000000;
        height: 400px;
        overflow: auto;
        padding: 4px;
    }
  </style>
</%def>

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if not bounce.processed and request.has_perm('emailbounces.process'):
      <li>${h.link_to("Mark this Email Bounce as Processed", url('emailbounces.process', uuid=bounce.uuid))}</li>
  % elif bounce.processed and request.has_perm('emailbounces.unprocess'):
      <li>${h.link_to("Mark this Email Bounce as UN-processed", url('emailbounces.unprocess', uuid=bounce.uuid))}</li>
  % endif
</%def>

<%def name="page_content()">
  ${parent.page_content()}
  <pre id="message">
  ${message}
  </pre>
</%def>


${parent.body()}
