## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    .field.is-horizontal .field-label .label {
        white-space: nowrap;
        min-width: 10rem;
    }
  </style>
</%def>

<%def name="page_content()">
  <profile-info @change-content-title="changeContentTitle">
  </profile-info>
</%def>

<%def name="render_this_page()">
  ${self.page_content()}
</%def>

<%def name="render_member_tab()">
  <b-tab-item label="Member" icon-pack="fas" :icon="members.length ? 'check' : null">

    <div v-if="members.length">

      <div style="display: flex; justify-content: space-between;">
        <p>{{ person.display_name }} is associated with <strong>{{ members.length }}</strong> member account(s)</p>
      </div>

      <br />
      <b-collapse v-for="member in members"
                  :key="member.uuid"
                  class="panel"
                  :open="members.length == 1">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
                  icon="caret-right">
          </b-icon>
          <strong>#{{ member.number }} {{ member.display }}</strong>
        </div>

        <div class="panel-block">
          <div style="display: flex; justify-content: space-between; width: 100%;">
            <div style="flex-grow: 1;">

              <b-field horizontal label="Number">
                {{ member.number }}
              </b-field>

              <b-field horizontal label="ID">
                {{ member.id }}
              </b-field>

              <b-field horizontal label="Active">
                {{ member.active }}
              </b-field>

              <b-field horizontal label="Joined">
                {{ member.joined }}
              </b-field>

              <b-field horizontal label="Withdrew"
                       v-if="member.withdrew">
                {{ member.withdrew }}
              </b-field>

              <b-field horizontal label="Person">
                <a v-if="member.person_uuid != person.uuid"
                   :href="member.view_profile_url">
                  {{ member.person_display_name }}
                </a>
                <span v-if="member.person_uuid == person.uuid">
                  {{ member.person_display_name }}
                </span>
              </b-field>

            </div>
            <div class="buttons" style="align-items: start;">
              ${self.render_member_panel_buttons(member)}
            </div>
          </div>
        </div>
      </b-collapse>
    </div>

    <div v-if="!members.length">
      <p>{{ person.display_name }} has never had a member account.</p>
    </div>

  </b-tab-item>
</%def>

<%def name="render_member_panel_buttons(member)">
  % if request.has_perm('members.view'):
      <b-button tag="a" :href="member.view_url">
        View Member
      </b-button>
  % endif
</%def>

<%def name="render_customer_tab()">
  <b-tab-item label="Customer" icon-pack="fas" :icon="customers.length ? 'check' : null">

    <div v-if="customers.length">

      <div style="display: flex; justify-content: space-between;">
        <p>{{ person.display_name }} is associated with <strong>{{ customers.length }}</strong> customer account(s)</p>
      </div>

      <br />
      <b-collapse v-for="customer in customers"
                  :key="customer.uuid"
                  class="panel"
                  :open="customers.length == 1">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
                  icon="caret-right">
          </b-icon>
          <strong>#{{ customer.number }} {{ customer.name }}</strong>
        </div>

        <div class="panel-block">
          <div style="display: flex; justify-content: space-between; width: 100%;">
            <div style="flex-grow: 1;">

              <b-field horizontal label="Number">
                {{ customer.number }}
              </b-field>

              <b-field horizontal label="ID">
                {{ customer.id }}
              </b-field>

              <b-field horizontal label="Name">
                {{ customer.name }}
              </b-field>

              <b-field horizontal label="People">
                <ul>
                  <li v-for="p in customer.people"
                      :key="p.uuid">
                    <a v-if="p.uuid != person.uuid"
                       :href="p.view_profile_url">
                      {{ p.display_name }}
                    </a>
                    <span v-if="p.uuid == person.uuid">
                      {{ p.display_name }}
                    </span>
                  </li>
                </ul>
              </b-field>

              <b-field horizontal label="Address"
                       v-for="address in customer.addresses"
                       :key="address.uuid">
                {{ address.display }}
              </b-field>

            </div>
            <div class="buttons" style="align-items: start;">
              ${self.render_customer_panel_buttons(customer)}
            </div>
          </div>
        </div>
      </b-collapse>
    </div>

    <div v-if="!customers.length">
      <p>{{ person.display_name }} has never had a customer account.</p>
    </div>

  </b-tab-item> <!-- Customer -->
</%def>

<%def name="render_customer_panel_buttons(customer)">
  % if request.has_perm('customers.view'):
      <b-button tag="a" :href="customer.view_url">
        View Customer
      </b-button>
  % endif
</%def>

<%def name="render_employee_tab_template()">
  <script type="text/x-template" id="employee-tab-template">
    <div>
      <div style="display: flex; justify-content: space-between;">

        <div style="flex-grow: 1;">

          <div v-if="employee.exists">

            <b-field horizontal label="Employee ID">
              <span>{{ employee.id }}</span>
            </b-field>

            <b-field horizontal label="Employee Status">
              <span>{{ employee.current ? "current" : "former" }}</span>
            </b-field>

            <b-field horizontal label="Start Date">
              <span>{{ employee.startDate }}</span>
            </b-field>

            <b-field horizontal label="End Date">
              <span>{{ employee.endDate }}</span>
            </b-field>

            <br />
            <p><strong>Employee History</strong></p>
            <br />

            <b-table :data="employeeHistory.data">
              <template slot-scope="props">

                <b-table-column field="start_date" label="Start Date">
                  {{ props.row.start_date }}
                </b-table-column>

                <b-table-column field="end_date" label="End Date">
                  {{ props.row.end_date }}
                </b-table-column>

                % if request.has_perm('people_profile.edit_employee_history'):
                    <b-table-column field="actions" label="Actions">
                      <a href="#" @click.prevent="editEmployeeHistory(props.row)">
                        <i class="fas fa-edit"></i>
                        Edit
                      </a>
                    </b-table-column>
                % endif

              </template>
            </b-table>

          </div>

          <p v-if="!employee.exists">
            ${person} has never been an employee.
          </p>

        </div>

        <div>
          <div class="buttons">

            % if request.has_perm('people_profile.toggle_employee'):

                <b-button v-if="!employee.current"
                          type="is-primary"
                          @click="showStartEmployee()">
                  ${person} is now an Employee
                </b-button>

                <b-button v-if="employee.current"
                          type="is-primary"
                          @click="showStopEmployeeDialog = true">
                  ${person} is no longer an Employee
                </b-button>

                <b-modal has-modal-card
                         :active.sync="showStartEmployeeDialog">
                  <div class="modal-card">

                    <header class="modal-card-head">
                      <p class="modal-card-title">Employee Start</p>
                    </header>

                    <section class="modal-card-body">
                      <b-field label="Employee Number">
                        <b-input v-model="employeeID"></b-input>
                      </b-field>
                      <b-field label="Start Date">
                        <tailbone-datepicker v-model="employeeStartDate"></tailbone-datepicker>
                      </b-field>
                    </section>

                    <footer class="modal-card-foot">
                      <b-button @click="showStartEmployeeDialog = false">
                        Cancel
                      </b-button>
                      <once-button type="is-primary"
                                   @click="startEmployee()"
                                   :disabled="!employeeStartDate"
                                   text="Save">
                      </once-button>
                    </footer>
                  </div>
                </b-modal>

                <b-modal has-modal-card
                         :active.sync="showStopEmployeeDialog">
                  <div class="modal-card">

                    <header class="modal-card-head">
                      <p class="modal-card-title">Employee End</p>
                    </header>

                    <section class="modal-card-body">
                      <b-field label="End Date"
                               :type="employeeEndDate ? null : 'is-danger'">
                        <tailbone-datepicker v-model="employeeEndDate"></tailbone-datepicker>
                      </b-field>
                      <b-field label="Revoke Internal App Access">
                        <b-checkbox v-model="employeeRevokeAccess">
                        </b-checkbox>
                      </b-field>
                    </section>

                    <footer class="modal-card-foot">
                      <b-button @click="showStopEmployeeDialog = false">
                        Cancel
                      </b-button>
                      <once-button type="is-primary"
                                   @click="endEmployee()"
                                   :disabled="!employeeEndDate"
                                   text="Save">
                      </once-button>
                    </footer>
                  </div>
                </b-modal>
            % endif

            % if request.has_perm('people_profile.edit_employee_history'):
                <b-modal has-modal-card
                         :active.sync="showEditEmployeeHistoryDialog">
                  <div class="modal-card">

                    <header class="modal-card-head">
                      <p class="modal-card-title">Edit Employee History</p>
                    </header>

                    <section class="modal-card-body">
                      <b-field label="Start Date">
                        <tailbone-datepicker v-model="employeeHistoryStartDate"></tailbone-datepicker>
                      </b-field>
                      <b-field label="End Date">
                        <tailbone-datepicker v-model="employeeHistoryEndDate"
                                             :disabled="!employeeHistoryEndDateRequired">
                        </tailbone-datepicker>
                      </b-field>
                    </section>

                    <footer class="modal-card-foot">
                      <b-button @click="showEditEmployeeHistoryDialog = false">
                        Cancel
                      </b-button>
                      <once-button type="is-primary"
                                   @click="saveEmployeeHistory()"
                                   :disabled="!employeeHistoryStartDate || (employeeHistoryEndDateRequired && !employeeHistoryEndDate)"
                                   text="Save">
                      </once-button>
                    </footer>
                  </div>
                </b-modal>
            % endif

            % if request.has_perm('employees.view'):
                <b-button v-if="employee.viewURL"
                          tag="a" :href="employee.viewURL">
                  View Employee
                </b-button>
            % endif

          </div>
        </div>

      </div>
    </div>
  </script>
</%def>

<%def name="render_employee_tab()">
  <b-tab-item label="Employee"
              icon-pack="fas"
              :icon="employee.current ? 'check' : null">
    <employee-tab :employee="employee"
                  :employee-history="employeeHistory"
                  @change-content-title="changeContentTitle">
    </employee-tab>
  </b-tab-item>
</%def>

<%def name="render_profile_info_template()">
  <script type="text/x-template" id="profile-info-template">
    <div>
      <b-tabs v-model="activeTab" type="is-boxed">

        <b-tab-item label="Personal" icon="check" icon-pack="fas">
          <div style="display: flex; justify-content: space-between;">

            <div>

              <div class="field-wrapper first_name">
                <div class="field-row">
                  <label>First Name</label>
                  <div class="field">
                    ${person.first_name}
                  </div>
                </div>
              </div>

              <div class="field-wrapper middle_name">
                <div class="field-row">
                  <label>Middle Name</label>
                  <div class="field">
                    ${person.middle_name}
                  </div>
                </div>
              </div>

              <div class="field-wrapper last_name">
                <div class="field-row">
                  <label>Last Name</label>
                  <div class="field">
                    ${person.last_name}
                  </div>
                </div>
              </div>

              <div class="field-wrapper street">
                <div class="field-row">
                  <label>Street 1</label>
                  <div class="field">
                    ${person.address.street if person.address else ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper street2">
                <div class="field-row">
                  <label>Street 2</label>
                  <div class="field">
                    ${person.address.street2 if person.address else ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper city">
                <div class="field-row">
                  <label>City</label>
                  <div class="field">
                    ${person.address.city if person.address else ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper state">
                <div class="field-row">
                  <label>State</label>
                  <div class="field">
                    ${person.address.state if person.address else ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper zipcode">
                <div class="field-row">
                  <label>Zipcode</label>
                  <div class="field">
                    ${person.address.zipcode if person.address else ''}
                  </div>
                </div>
              </div>

              % if person.phones:
                  % for phone in person.phones:
                      <div class="field-wrapper">
                        <div class="field-row">
                          <label>Phone Number</label>
                          <div class="field">
                            ${phone.number} (type: ${phone.type})
                          </div>
                        </div>
                      </div>
                  % endfor
              % else:
                  <div class="field-wrapper">
                    <div class="field-row">
                      <label>Phone Number</label>
                      <div class="field">
                        (none on file)
                      </div>
                    </div>
                  </div>
              % endif

              % if person.emails:
                  % for email in person.emails:
                      <div class="field-wrapper">
                        <div class="field-row">
                          <label>Email Address</label>
                          <div class="field">
                            ${email.address} (type: ${email.type})
                          </div>
                        </div>
                      </div>
                  % endfor
              % else:
                  <div class="field-wrapper">
                    <div class="field-row">
                      <label>Email Address</label>
                      <div class="field">
                        (none on file)
                      </div>
                    </div>
                  </div>
              % endif

            </div>

            <div>
              % if request.has_perm('people.view'):
                  ${h.link_to("View Person", url('people.view', uuid=person.uuid), class_='button')}
              % endif
            </div>

          </div>
        </b-tab-item><!-- Personal -->

        ${self.render_customer_tab()}

        ${self.render_member_tab()}

        ${self.render_employee_tab()}

        <b-tab-item label="User" ${'icon="check" icon-pack="fas"' if person.users else ''|n}>
          % if person.users:
              <p>${person} is associated with <strong>${len(person.users)}</strong> user account(s)</p>
              <br />
              <div id="users-accordion">
                % for user in person.users:

                    <b-collapse class="panel"
                                ## TODO: what's up with aria-id here?
                                ## aria-id="contentIdForA11y2"
                                >

                      <div
                         slot="trigger"
                         class="panel-heading"
                         role="button"
                         ## TODO: what's up with aria-id here?
                         ## aria-controls="contentIdForA11y2"
                         >
                        <strong>${user.username}</strong>
                      </div>

                      <div class="panel-block">

                        <div style="display: flex; justify-content: space-between; width: 100%;">

                          <div>

                            <div class="field-wrapper id">
                              <div class="field-row">
                                <label>Username</label>
                                <div class="field">
                                  ${user.username}
                                </div>
                              </div>
                            </div>

                          </div>

                          <div>
                            % if request.has_perm('users.view'):
                                ${h.link_to("View User", url('users.view', uuid=user.uuid), class_='button')}
                            % endif
                          </div>

                        </div>

                      </div>
                    </b-collapse>
                % endfor
              </div>

          % else:
              <p>${person} has never been a user.</p>
          % endif
        </b-tab-item><!-- User -->

      </b-tabs>
    </div>
  </script>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  ${self.render_employee_tab_template()}
  ${self.render_profile_info_template()}
</%def>

<%def name="set_employee_data()">
  <script type="text/javascript">

    let EmployeeData = {
        exists: ${json.dumps(bool(employee))|n},
        viewURL: ${json.dumps(employee_view_url)|n},
        current: ${json.dumps(bool(employee and employee.status == enum.EMPLOYEE_STATUS_CURRENT))|n},
        startDate: ${json.dumps(six.text_type(employee_history.start_date) if employee_history else None)|n},
        endDate: ${json.dumps(six.text_type(employee_history.end_date) if employee_history and employee_history.end_date else None)|n},
        id: ${json.dumps(employee.id if employee else None)|n},
    }

    let EmployeeHistoryData = {
        data: ${json.dumps(employee_history_data)|n},
    }

  </script>
</%def>

<%def name="declare_employee_tab_vars()">
  <script type="text/javascript">

    let EmployeeTab = {
        template: '#employee-tab-template',
        props: {
            employee: Object,
            employeeHistory: Object,
        },
        data() {
            return {
                showStartEmployeeDialog: false,
                employeeID: null,
                employeeStartDate: null,
                showStopEmployeeDialog: false,
                employeeEndDate: null,
                employeeRevokeAccess: false,
                showEditEmployeeHistoryDialog: false,
                employeeHistoryUUID: null,
                employeeHistoryStartDate: null,
                employeeHistoryEndDate: null,
                employeeHistoryEndDateRequired: false,

                ## TODO: should find a better way to handle CSRF token
                csrftoken: ${json.dumps(request.session.get_csrf_token() or request.session.new_csrf_token())|n},
            }
        },

        methods: {

            changeContentTitle(newTitle) {
                this.$emit('change-content-title', newTitle)
            },

            % if request.has_perm('people_profile.toggle_employee'):

                showStartEmployee() {
                    this.employeeID = this.employee.id
                    this.showStartEmployeeDialog = true
                },

                startEmployee() {

                    let url = '${url('people.profile_start_employee', uuid=person.uuid)}'

                    let params = {
                        id: this.employeeID,
                        start_date: this.employeeStartDate,
                    }

                    let headers = {
                        ## TODO: should find a better way to handle CSRF token
                        'X-CSRF-TOKEN': this.csrftoken,
                    }

                    ## TODO: should find a better way to handle CSRF token
                    this.$http.post(url, params, {headers: headers}).then(({ data }) => {
                        if (data.success) {
                            this.startEmployeeSuccess(data)
                        } else {
                            this.$buefy.toast.open({
                                message: "Save failed:  " + data.error,
                                type: 'is-danger',
                                duration: 4000, // 4 seconds
                            })
                        }
                    }, response => {
                        alert("Unexpected error occurred!")
                    })
                },

                startEmployeeSuccess(data) {
                    this.employee.exists = true
                    this.employee.id = data.employee_id
                    this.employee.viewURL = data.employee_view_url
                    this.employee.current = true
                    this.employee.startDate = data.start_date
                    this.employee.endDate = null
                    this.employeeHistory.data = data.employee_history_data
                    // this.customerNumber = data.customer_number
                    this.employeeEndDate = null
                    this.$emit('change-content-title', data.dynamic_content_title)
                    // this.posTabStale = true
                    this.showStartEmployeeDialog = false
                },

                endEmployee() {

                    let url = '${url('people.profile_end_employee', uuid=person.uuid)}'

                    let params = {
                        end_date: this.employeeEndDate,
                        revoke_access: this.employeeRevokeAccess,
                    }

                    let headers = {
                        ## TODO: should find a better way to handle CSRF token
                        'X-CSRF-TOKEN': this.csrftoken,
                    }

                    ## TODO: should find a better way to handle CSRF token
                    this.$http.post(url, params, {headers: headers}).then(({ data }) => {
                        if (data.success) {
                            this.endEmployeeSuccess(data)
                        } else {
                            this.$buefy.toast.open({
                                message: "Save failed:  " + data.error,
                                type: 'is-danger',
                                duration: 4000, // 4 seconds
                            })
                        }
                    }, response => {
                        alert("Unexpected error occurred!")
                    })
                },

                endEmployeeSuccess(data) {
                    this.employee.current = false
                    this.employee.endDate = data.end_date
                    this.employeeHistory.data = data.employee_history_data
                    this.employeeStartDate = null
                    this.$emit('change-content-title', data.dynamic_content_title)
                    // this.memberTabStale = true
                    // this.posTabStale = true
                    this.showStopEmployeeDialog = false
                },

            % endif

            % if request.has_perm('people_profile.edit_employee_history'):

                editEmployeeHistory(row) {
                    this.employeeHistoryUUID = row.uuid
                    this.employeeHistoryStartDate = row.start_date
                    this.employeeHistoryEndDate = row.end_date
                    this.employeeHistoryEndDateRequired = !!row.end_date
                    this.showEditEmployeeHistoryDialog = true
                },

                saveEmployeeHistory() {

                    let url = '${url('people.profile_edit_employee_history', uuid=person.uuid)}'

                    let params = {
                        uuid: this.employeeHistoryUUID,
                        start_date: this.employeeHistoryStartDate,
                        end_date: this.employeeHistoryEndDate,
                    }

                    let headers = {
                        ## TODO: should find a better way to handle CSRF token
                        'X-CSRF-TOKEN': this.csrftoken,
                    }

                    ## TODO: should find a better way to handle CSRF token
                    this.$http.post(url, params, {headers: headers}).then(({ data }) => {
                        if (data.success) {
                            this.employee.startDate = data.start_date
                            this.employee.endDate = data.end_date
                            this.employeeHistory.data = data.employee_history_data
                        }
                        this.showEditEmployeeHistoryDialog = false
                    })
                },

            % endif
        },
    }

  </script>
</%def>

<%def name="make_employee_tab_component()">
  ${self.declare_employee_tab_vars()}
  <script type="text/javascript">

    Vue.component('employee-tab', EmployeeTab)

  </script>
</%def>

<%def name="make_profile_info_component()">
  <script type="text/javascript">

    const ProfileInfo = {
        template: '#profile-info-template',
        data() {
            return {
                activeTab: 0,
                person: ${json.dumps(person_data)|n},
                customers: ${json.dumps(customers_data)|n},
                members: ${json.dumps(members_data)|n},
                employee: EmployeeData,
                employeeHistory: EmployeeHistoryData,
            }
        },
        methods: {
            changeContentTitle(newTitle) {
                this.$emit('change-content-title', newTitle)
            },
        },
    }

    Vue.component('profile-info', ProfileInfo)

  </script>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPage.methods.changeContentTitle = function(newTitle) {
        this.$emit('change-content-title', newTitle)
    }

  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  ${self.set_employee_data()}
  ${self.make_employee_tab_component()}
  ${self.make_profile_info_component()}
</%def>


${parent.body()}
