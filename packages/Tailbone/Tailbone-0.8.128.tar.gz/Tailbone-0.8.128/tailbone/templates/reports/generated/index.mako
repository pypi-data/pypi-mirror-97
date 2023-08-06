## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('{}.generate'.format(permission_prefix)):
      <li>${h.link_to("Generate new Report", url('generate_report'))}</li>
  % endif
</%def>

${parent.body()}
