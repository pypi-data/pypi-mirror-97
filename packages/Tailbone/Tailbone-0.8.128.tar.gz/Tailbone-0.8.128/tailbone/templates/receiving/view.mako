## -*- coding: utf-8; -*-
<%inherit file="/batch/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if master.has_perm('edit_row'):
      ${h.javascript_link(request.static_url('tailbone:static/js/numeric.js'))}
      <script type="text/javascript">

        % if not batch.executed:
        // keep track of which cost value is currently being edited
        var editing_catalog_cost = null;
        var editing_invoice_cost = null;

        function start_editing(td) {
            var value = null;
            var text = td.text().replace(/^\s+|\s+$/g, '');
            if (text) {
                td.data('previous-value', text);
                td.text('');
                value = parseFloat(text.replace('$', ''));
            }
            var input = $('<input type="text" />');
            td.append(input);
            value = value ? value.toString() : '';
            input.val(value).select().focus();
        }

        function start_editing_catalog_cost(td) {
            start_editing(td);
            editing_catalog_cost = td;
        }

        function start_editing_invoice_cost(td) {
            start_editing(td);
            editing_invoice_cost = td;
        }

        function start_editing_next_catalog_cost() {
            var tr = editing_catalog_cost.parents('tr:first');
            var next = tr.next('tr:first');
            if (next.length) {
                start_editing_catalog_cost(next.find('td.catalog_unit_cost'));
            } else {
                editing_catalog_cost = null;
            }
        }

        function start_editing_next_invoice_cost() {
            var tr = editing_invoice_cost.parents('tr:first');
            var next = tr.next('tr:first');
            if (next.length) {
                start_editing_invoice_cost(next.find('td.invoice_unit_cost'));
            } else {
                editing_invoice_cost = null;
            }
        }

        function cancel_edit(td) {
            var input = td.find('input');
            input.blur();
            input.remove();
            var value = td.data('previous-value');
            if (value) {
                td.text(value);
            }
        }

        function cancel_edit_catalog_cost() {
            cancel_edit(editing_catalog_cost);
            editing_catalog_cost = null;
        }

        function cancel_edit_invoice_cost() {
            cancel_edit(editing_invoice_cost);
            editing_invoice_cost = null;
        }

        % endif

        $(function() {

            % if not batch.executed:
            $('.grid-wrapper').on('click', '.grid td.catalog_unit_cost', function() {
                if (editing_catalog_cost) {
                    editing_catalog_cost.find('input').focus();
                    return
                }
                if (editing_invoice_cost) {
                    editing_invoice_cost.find('input').focus();
                    return
                }
                var td = $(this);
                start_editing_catalog_cost(td);
            });

            $('.grid-wrapper').on('click', '.grid td.invoice_unit_cost', function() {
                if (editing_invoice_cost) {
                    editing_invoice_cost.find('input').focus();
                    return
                }
                if (editing_catalog_cost) {
                    editing_catalog_cost.find('input').focus();
                    return
                }
                var td = $(this);
                start_editing_invoice_cost(td);
            });

            $('.grid-wrapper').on('keyup', '.grid td.catalog_unit_cost input', function(event) {
                var input = $(this);

                // let numeric keys modify input value
                if (! key_modifies(event)) {

                    // when user presses Enter while editing cost value, submit
                    // value to server for immediate persistence
                    if (event.which == 13) {
                        $('.grid-wrapper').mask("Updating cost...");
                        var url = '${url('receiving.update_row_cost', uuid=batch.uuid)}';
                        var td = input.parents('td:first');
                        var tr = td.parents('tr:first');
                        var data = {
                            '_csrf': $('[name="_csrf"]').val(),
                            'row_uuid': tr.data('uuid'),
                            'catalog_unit_cost': input.val()
                        };
                        $.post(url, data, function(data) {
                            if (data.error) {
                                alert(data.error);
                            } else {
                                var total = null;

                                // update catalog cost for row
                                td.text(data.row.catalog_unit_cost);

                                // mark cost as confirmed
                                if (data.row.catalog_cost_confirmed) {
                                    tr.addClass('catalog_cost_confirmed');
                                }

                                input.blur();
                                input.remove();
                                start_editing_next_catalog_cost();
                            }
                            $('.grid-wrapper').unmask();
                        });

                    // When user presses Escape while editing totals, cancel the edit.
                    } else if (event.which == 27) {
                        cancel_edit_catalog_cost();

                    // Most other keys at this point should be unwanted...
                    } else if (! key_allowed(event)) {
                        return false;
                    }
                }
            });

            $('.grid-wrapper').on('keyup', '.grid td.invoice_unit_cost input', function(event) {
                var input = $(this);

                // let numeric keys modify input value
                if (! key_modifies(event)) {

                    // when user presses Enter while editing cost value, submit
                    // value to server for immediate persistence
                    if (event.which == 13) {
                        $('.grid-wrapper').mask("Updating cost...");
                        var url = '${url('receiving.update_row_cost', uuid=batch.uuid)}';
                        var td = input.parents('td:first');
                        var tr = td.parents('tr:first');
                        var data = {
                            '_csrf': $('[name="_csrf"]').val(),
                            'row_uuid': tr.data('uuid'),
                            'invoice_unit_cost': input.val()
                        };
                        $.post(url, data, function(data) {
                            if (data.error) {
                                alert(data.error);
                            } else {
                                var total = null;

                                // update unit cost for row
                                td.text(data.row.invoice_unit_cost);

                                // update invoice total for row
                                total = tr.find('td.invoice_total_calculated');
                                total.text('$' + data.row.invoice_total_calculated);

                                // update invoice total for batch
                                total = $('.form .field-wrapper.invoice_total_calculated .field');
                                total.text('$' + data.batch.invoice_total_calculated);

                                // mark cost as confirmed
                                if (data.row.invoice_cost_confirmed) {
                                    tr.addClass('invoice_cost_confirmed');
                                }

                                input.blur();
                                input.remove();
                                start_editing_next_invoice_cost();
                            }
                            $('.grid-wrapper').unmask();
                        });

                    // When user presses Escape while editing totals, cancel the edit.
                    } else if (event.which == 27) {
                        cancel_edit_invoice_cost();

                    // Most other keys at this point should be unwanted...
                    } else if (! key_allowed(event)) {
                        return false;
                    }
                }
            });
            % endif

            $('.grid-wrapper').on('click', '.grid .actions a.transform', function() {

                var form = $('form[name="transform-unit-form"]');
                var row_uuid = $(this).parents('tr:first').data('uuid');
                form.find('[name="row_uuid"]').val(row_uuid);

                $.get(form.attr('action'), {row_uuid: row_uuid}, function(data) {

                    if (typeof(data) == 'object') {
                        alert(data.error);

                    } else {
                        $('#transform-unit-dialog').html(data);
                        $('#transform-unit-dialog').dialog({
                            title: "Transform Pack to Unit Item",
                            width: 800,
                            height: 450,
                            modal: true,
                            buttons: [
                                {
                                    text: "Transform",
                                    click: function(event) {
                                        disable_button(dialog_button(event));
                                        form.submit();
                                    }
                                },
                                {
                                    text: "Cancel",
                                    click: function() {
                                        $(this).dialog('close');
                                    }
                                }
                            ]
                        });
                    }
                });

                return false;
            });

        });

      </script>
  % endif
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  % if not batch.executed and master.has_perm('edit_row'):
      <style type="text/css">
        .grid tr:not(.header) td.catalog_unit_cost,
        .grid tr:not(.header) td.invoice_unit_cost {
          cursor: pointer;
          background-color: #fcc;
        }
        .grid tr.catalog_cost_confirmed:not(.header) td.catalog_unit_cost,
        .grid tr.invoice_cost_confirmed:not(.header) td.invoice_unit_cost {
          background-color: #cfc;
        }
        .grid td.catalog_unit_cost input,
        .grid td.invoice_unit_cost input {
          width: 4rem;
        }
      </style>
  % endif
</%def>

<%def name="object_helpers()">
  ${parent.object_helpers()}
  ## TODO: for now this is a truck-dump-only feature? maybe should change that
  % if not request.rattail_config.production() and master.handler.allow_truck_dump_receiving():
      % if not batch.executed and not batch.complete and request.has_perm('admin'):
          % if (batch.is_truck_dump_parent() and batch.truck_dump_children_first) or not batch.is_truck_dump_related():
              <div class="object-helper">
                <h3>Development Tools</h3>
                <div class="object-helper-content">
                  % if use_buefy:
                      ${h.form(url('{}.auto_receive'.format(route_prefix), uuid=batch.uuid), ref='auto_receive_all_form')}
                      ${h.csrf_token(request)}
                      <once-button type="is-primary"
                                   @click="$refs.auto_receive_all_form.submit()"
                                   text="Auto-Receive All Items">
                      </once-button>
                      ${h.end_form()}
                  % else:
                      ${h.form(url('{}.auto_receive'.format(route_prefix), uuid=batch.uuid), class_='autodisable')}
                      ${h.csrf_token(request)}
                      ${h.submit('submit', "Auto-Receive All Items")}
                      ${h.end_form()}
                  % endif
                </div>
              </div>
          % endif
      % endif
  % endif
</%def>


${parent.body()}

% if master.handler.allow_truck_dump_receiving() and master.has_perm('edit_row'):
    ${h.form(url('{}.transform_unit_row'.format(route_prefix), uuid=batch.uuid), name='transform-unit-form')}
    ${h.csrf_token(request)}
    ${h.hidden('row_uuid')}
    ${h.end_form()}

    <div id="transform-unit-dialog" style="display: none;">
      <p>hello world</p>
    </div>
% endif
