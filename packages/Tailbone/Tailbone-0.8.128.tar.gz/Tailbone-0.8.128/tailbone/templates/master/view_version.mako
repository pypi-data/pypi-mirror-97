## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">changes @ ver ${transaction.id}</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">

    .this-page-content {
        overflow: auto;
    }

  </style>
</%def>

<%def name="page_content()">
## TODO: this was basically copied from Revel diff template..need to abstract

<div class="form-wrapper">

  <div class="form">

    <div class="field-wrapper">
      <label>Changed</label>
      <div class="field">${h.pretty_datetime(request.rattail_config, changed)}</div>
    </div>

    <div class="field-wrapper">
      <label>Changed by</label>
      <div class="field">${transaction.user or ''}</div>
    </div>

    <div class="field-wrapper">
      <label>IP Address</label>
      <div class="field">${transaction.remote_addr}</div>
    </div>

    <div class="field-wrapper">
      <label>Comment</label>
      <div class="field">${transaction.meta.get('comment') or ''}</div>
    </div>

  </div>

</div><!-- form-wrapper -->

% for version in versions:

    <h2>${title_for_version(version)}</h2>

    % if version.previous and version.operation_type == continuum.Operation.DELETE:
        <table class="diff monospace deleted">
          <thead>
            <tr>
              <th>field name</th>
              <th>old value</th>
              <th>new value</th>
            </tr>
          </thead>
          <tbody>
            % for field in fields_for_version(version):
               <tr>
                 <td class="field">${field}</td>
                 <td class="value old-value">${repr(getattr(version.previous, field))}</td>
                 <td class="value new-value">&nbsp;</td>
               </tr>
            % endfor
          </tbody>
        </table>
    % elif version.previous:
        <table class="diff monospace dirty">
          <thead>
            <tr>
              <th>field name</th>
              <th>old value</th>
              <th>new value</th>
            </tr>
          </thead>
          <tbody>
            % for field in fields_for_version(version):
               <tr${' class="diff"' if getattr(version, field) != getattr(version.previous, field) else ''|n}>
                 <td class="field">${field}</td>
                 <td class="value old-value">${repr(getattr(version.previous, field))}</td>
                 <td class="value new-value">${repr(getattr(version, field))}</td>
               </tr>
            % endfor
          </tbody>
        </table>
    % else:
        <table class="diff monospace new">
          <thead>
            <tr>
              <th>field name</th>
              <th>old value</th>
              <th>new value</th>
            </tr>
          </thead>
          <tbody>
            % for field in fields_for_version(version):
               <tr>
                 <td class="field">${field}</td>
                 <td class="value old-value">&nbsp;</td>
                 <td class="value new-value">${repr(getattr(version, field))}</td>
               </tr>
            % endfor
          </tbody>
        </table>
    % endif

% endfor
</%def>


${parent.body()}
