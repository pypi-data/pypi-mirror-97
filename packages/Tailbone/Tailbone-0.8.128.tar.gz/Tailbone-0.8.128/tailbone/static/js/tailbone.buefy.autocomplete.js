
const TailboneAutocomplete = {

    template: '#tailbone-autocomplete-template',

    props: {
        name: String,
        serviceUrl: String,
        value: String,
        initialLabel: String,
        assignedValue: String,
        assignedLabel: String,
    },

    data() {
        let selected = null
        if (this.value) {
            selected = {
                value: this.value,
                label: this.initialLabel,
            }
        }
        return {
            data: [],
            selected: selected,
            isFetching: false,
        }
    },

    watch: {
        value(to, from) {
            if (from && !to) {
                this.clearSelection(false)
            }
        },
    },

    methods: {

        clearSelection(focus) {
            if (focus === undefined) {
                focus = true
            }
            this.selected = null
            this.value = null
            if (focus) {
                this.$nextTick(function() {
                    this.focus()
                })
            }

            // TODO: should emit event for caller logic (can they cancel?)
            // $('#' + oid + '-textbox').trigger('autocompletevaluecleared');
        },

        focus() {
            this.$refs.autocomplete.focus()
        },

        getDisplayText() {
            if (this.selected) {
                return this.selected.label
            }
            return ""
        },

        // TODO: should we allow custom callback? or is event enough?
        // function (oid) {
        //     $('#' + oid + '-textbox').on('autocompletevaluecleared', function() {
        //         ${cleared_callback}();
        //     });
        // }

        selectionMade(option) {
            this.selected = option

            // TODO: should emit event for caller logic (can they cancel?)
            // $('#' + oid + '-textbox').trigger('autocompletevalueselected',
            //                                   [ui.item.value, ui.item.label]);
        },

        // TODO: should we allow custom callback? or is event enough?
        // function (oid) {
        //     $('#' + oid + '-textbox').on('autocompletevalueselected', function(event, uuid, label) {
        //         ${selected_callback}(uuid, label);
        //     });
        // }

        itemSelected(value) {
            if (this.selected || !value) {
                this.$emit('input', value)
            }
        },

        // TODO: buefy example uses `debounce()` here and perhaps we should too?
        // https://buefy.org/documentation/autocomplete
        getAsyncData: function (entry) {
            if (entry.length < 3) {
                this.data = []
                return
            }
            this.isFetching = true
            this.$http.get(this.serviceUrl + '?term=' + encodeURIComponent(entry))
                .then(({ data }) => {
                    this.data = data
                })
                .catch((error) => {
                    this.data = []
                    throw error
                })
                    .finally(() => {
                        this.isFetching = false
                    })
                        },
    },
}

Vue.component('tailbone-autocomplete', TailboneAutocomplete)
