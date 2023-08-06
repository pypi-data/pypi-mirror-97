## -*- coding: utf-8; -*-

<script type="text/x-template" id="${form.component}-template">

  <div>
  % if not form.readonly:
  ${h.form(form.action_url, id=dform.formid, method='post', enctype='multipart/form-data', **form_kwargs)}
  ${h.csrf_token(request)}
  % endif

  <section>
    % for field in form.fields:
        % if form.readonly or (field not in dform and field in form.readonly_fields):
            <b-field horizontal
                     label="${form.get_label(field)}">
              ${form.render_field_value(field) or h.HTML.tag('span')}
            </b-field>

        % elif field in dform:
            <% field = dform[field] %>

            % if form.field_visible(field.name):
                <b-field horizontal
                         label="${form.get_label(field.name)}"
                         ## TODO: is this class="file" really needed?
                         % if isinstance(field.schema.typ, deform.FileData):
                         class="file"
                         % endif
                         % if field.error:
                         type="is-danger"
                         :message='${form.messages_json(field.error.messages())|n}'
                         % endif
                         >
                  ${field.serialize(use_buefy=True)|n}
                </b-field>
            % else:
                ## hidden field
                ${field.serialize()|n}
            % endif
        % endif

    % endfor
  </section>

  % if buttons:
      <br />
      ${buttons|n}
  % elif not form.readonly and (buttons is Undefined or (buttons is not None and buttons is not False)):
      <br />
      <div class="buttons">
        ## TODO: deprecate / remove the latter option here
        % if form.auto_disable_save or form.auto_disable:
            <b-button type="is-primary"
                      native-type="submit"
                      :disabled="${form.component_studly}Submitting">
              {{ ${form.component_studly}ButtonText }}
            </b-button>
        % else:
            <b-button type="is-primary"
                      native-type="submit">
              ${getattr(form, 'submit_label', getattr(form, 'save_label', "Submit"))}
            </b-button>
        % endif
        % if getattr(form, 'show_reset', False):
            <input type="reset" value="Reset" class="button" />
        % endif
        % if getattr(form, 'show_cancel', True):
            % if form.auto_disable_cancel:
                <once-button tag="a" href="${form.cancel_url or request.get_referrer()}"
                             text="Cancel">
                </once-button>
            % else:
                <b-button tag="a" href="${form.cancel_url or request.get_referrer()}">
                  Cancel
                </b-button>
            % endif
        % endif
      </div>
  % endif

  % if not form.readonly:
  ${h.end_form()}
  % endif
  </div>
</script>

<script type="text/javascript">

  let ${form.component_studly} = {
      template: '#${form.component}-template',
      components: {},
      props: {},
      methods: {

          ## TODO: deprecate / remove the latter option here
          % if form.auto_disable_save or form.auto_disable:
              submit${form.component_studly}() {
                  this.${form.component_studly}Submitting = true
                  this.${form.component_studly}ButtonText = "Working, please wait..."
              }
          % endif
      }
  }

  let ${form.component_studly}Data = {

      ## TODO: ugh, this seems pretty hacky.  need to declare some data models
      ## for various field components to bind to...
      % if not form.readonly:
          % for field in form.fields:
              % if field in dform:
                  <% field = dform[field] %>
                  field_model_${field.name}: ${form.get_vuejs_model_value(field)|n},
              % endif
          % endfor
      % endif

      ## TODO: deprecate / remove the latter option here
      % if form.auto_disable_save or form.auto_disable:
          ${form.component_studly}Submitting: false,
          ${form.component_studly}ButtonText: ${json.dumps(getattr(form, 'submit_label', getattr(form, 'save_label', "Submit")))|n},
      % endif
  }

</script>
