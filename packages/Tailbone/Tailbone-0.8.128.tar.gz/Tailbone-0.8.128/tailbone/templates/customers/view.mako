## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />
<%namespace file="/util.mako" import="view_profiles_helper" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if master.people_detachable and request.has_perm('{}.detach_person'.format(permission_prefix)):
      <script type="text/javascript">

        $(function() {
            $('.people .grid .actions a.detach').click(function() {
                if (! confirm("Are you sure you wish to detach this Person from the Customer?")) {
                    return false;
                }
            });
        });

      </script>
  % endif
</%def>

<%def name="object_helpers()">
  ${parent.object_helpers()}
  % if show_profiles_helper and instance.people:
      ${view_profiles_helper(instance.people)}
  % endif
</%def>

${parent.body()}
