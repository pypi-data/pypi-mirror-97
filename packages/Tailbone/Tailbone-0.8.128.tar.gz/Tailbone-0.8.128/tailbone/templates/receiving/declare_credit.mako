## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Declare Credit for Row #${row.sequence}</%def>

<%def name="context_menu_items()">
  % if master.rows_viewable and request.has_perm('{}.view'.format(permission_prefix)):
      <li>${h.link_to("View this {}".format(row_model_title), row_action_url('view', row))}</li>
  % endif
</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    function toggleFields(creditType) {
        if (creditType === undefined) {
            creditType = $('select[name="credit_type"]').val();
        }
        if (creditType == 'expired') {
            $('.field-wrapper.expiration_date').show();
        } else {
            $('.field-wrapper.expiration_date').hide();
        }
    }

    $(function() {

        toggleFields();

        $('select[name="credit_type"]').on('selectmenuchange', function(event, ui) {
            toggleFields(ui.item.value);
        });

    });
  </script>
</%def>

<div style="display: flex; justify-content: space-between;">

  <div class="form-wrapper">

    <p style="padding: 1em;">
      Please select the "state" of the product, and enter the appropriate
      quantity.
    </p>

    <p style="padding: 1em;">
      Note that this tool will <strong>deduct</strong> from the "received"
      quantity, and <strong>add</strong> to the corresponding credit quantity.
    </p>

    <p style="padding: 1em;">
      Please see ${h.link_to("Receive Row", url('{}.receive_row'.format(route_prefix), uuid=batch.uuid, row_uuid=row.uuid))}
      if you need to "receive" instead of "convert" the product.
    </p>

    ${form.render()|n}
  </div><!-- form-wrapper -->

  <ul id="context-menu">
    ${self.context_menu_items()}
  </ul>

</div>
