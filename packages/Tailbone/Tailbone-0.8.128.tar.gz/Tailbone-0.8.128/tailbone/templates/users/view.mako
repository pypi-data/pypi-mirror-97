## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />
<%namespace file="/util.mako" import="view_profiles_helper" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/perms.css'))}
</%def>

<%def name="object_helpers()">
  ${parent.object_helpers()}
  % if instance.person:
      ${view_profiles_helper([instance.person])}
  % endif
</%def>

${parent.body()}
