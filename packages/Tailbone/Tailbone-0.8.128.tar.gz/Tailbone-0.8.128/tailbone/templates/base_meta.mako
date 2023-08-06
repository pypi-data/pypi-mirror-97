## -*- coding: utf-8; -*-

<%def name="app_title()">${request.rattail_config.node_title(default="Rattail")}</%def>

<%def name="global_title()">${"[STAGE] " if not request.rattail_config.production() else ''}${self.app_title()}</%def>

<%def name="favicon()">
  <link rel="icon" type="image/x-icon" href="${request.static_url('tailbone:static/img/rattail.ico')}" />
</%def>

<%def name="header_logo()"></%def>

<%def name="footer()">
  <p class="has-text-centered">
    powered by ${h.link_to("Rattail", url('about'))}
  </p>
</%def>
