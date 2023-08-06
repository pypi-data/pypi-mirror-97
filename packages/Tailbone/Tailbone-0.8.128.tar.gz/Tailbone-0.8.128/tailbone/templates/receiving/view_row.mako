## -*- coding: utf-8; -*-
<%inherit file="/master/view_row.mako" />

<%def name="object_helpers()">
  ${parent.object_helpers()}
  % if not batch.executed and not batch.is_truck_dump_child():
      <div class="object-helper">
        <h3>Receiving Tools</h3>
        <div class="object-helper-content">
          <div style="white-space: nowrap;">
            ${h.link_to("Receive Product", url('{}.receive_row'.format(route_prefix), uuid=batch.uuid, row_uuid=row.uuid), class_='button autodisable')}
            ${h.link_to("Declare Credit", url('{}.declare_credit'.format(route_prefix), uuid=batch.uuid, row_uuid=row.uuid), class_='button autodisable')}
          </div>
        </div>
      </div>
  % endif
</%def>

${parent.body()}
