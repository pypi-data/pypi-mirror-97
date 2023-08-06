## -*- coding: utf-8; -*-

<%def name="view_profile_button(person)">
  <div class="buttons">
    ${h.link_to(person, url('people.view_profile', uuid=person.uuid), class_='button is-primary')}
  </div>
</%def>

<%def name="view_profiles_helper(people)">
  % if request.has_perm('people.view_profile'):
      <div class="object-helper">
        <h3>Profiles</h3>
        <div class="object-helper-content">
          <p>View full profile for:</p>
          % for person in people:
              ${view_profile_button(person)}
          % endfor
        </div>
      </div>
  % endif
</%def>
