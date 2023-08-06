## -*- coding: utf-8; -*-

<%def name="declare_formposter_mixin()">
  <script type="text/javascript">

    let FormPosterMixin = {
        methods: {

            submitForm(action, params, success) {

                let csrftoken = ${json.dumps(request.session.get_csrf_token() or request.session.new_csrf_token())|n}

                let headers = {
                    '${csrf_header_name}': csrftoken,
                }

                this.$http.post(action, params, {headers: headers}).then(response => {

                    if (response.data.ok) {
                        success(response)

                    } else {
                        this.$buefy.toast.open({
                            message: "Failed to send feedback:  " + response.data.error,
                            type: 'is-danger',
                            duration: 4000, // 4 seconds
                        })
                    }

                }, response => {
                    this.$buefy.toast.open({
                        message: "Failed to submit form!  (unknown server error)",
                        type: 'is-danger',
                        duration: 4000, // 4 seconds
                    })
                })
            },
        },
    }

  </script>
</%def>
